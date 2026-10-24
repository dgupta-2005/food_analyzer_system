import os
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models.product import PackagedProduct, StatisticalComparison
from app.schemas.product import (
    ProductNutritionSchema,
    BarcodeScanResponse,
    StatisticalComparisonSchema
)
from app.services.storage_service import storage_service
from app.services.scanner_service import scanner_service
from app.services.comparison_service import comparison_engine

router = APIRouter(prefix="/packaged-food", tags=["Packaged Food & Healthy Alternatives"])

@router.post("/scan-barcode", response_model=BarcodeScanResponse)
async def scan_barcode_image(image: UploadFile = File(...)):
    """
    UC-2 Scan Service: Uploads packaged food barcode photo, decodes barcode via zxingcpp,
    and returns nutrition breakdown from OpenFoodFacts database.
    """
    saved_url = await storage_service.save_file(image, subfolder="barcodes")
    local_path = saved_url.replace("/uploads/", str(storage_service.upload_dir) + "/") if saved_url.startswith("/uploads/") else None

    if not local_path or not os.path.exists(local_path):
        raise HTTPException(status_code=400, detail="Failed to save uploaded image.")

    barcode = scanner_service.scan_barcode_from_image_path(local_path)
    if not barcode:
        return BarcodeScanResponse(
            barcode=None,
            success=False,
            message="No barcode stripe detected in image. Try uploading a clearer picture or search by product name."
        )

    product = await scanner_service.fetch_product_by_barcode(barcode)
    if not product:
        return BarcodeScanResponse(
            barcode=barcode,
            success=False,
            message=f"Barcode '{barcode}' decoded but product was not found in OpenFoodFacts database."
        )

    return BarcodeScanResponse(
        barcode=barcode,
        success=True,
        message="Product successfully decoded and retrieved.",
        product=product
    )

@router.get("/lookup/{barcode}", response_model=ProductNutritionSchema)
async def lookup_barcode_number(barcode: str, db: AsyncSession = Depends(get_db)):
    """UC-2 Lookup: Direct numeric barcode query."""
    # Check database cache first
    stmt = select(PackagedProduct).where(PackagedProduct.barcode == barcode)
    res = await db.execute(stmt)
    db_prod = res.scalar_one_or_none()

    if db_prod:
        return ProductNutritionSchema.model_validate(db_prod)

    # Fetch from OpenFoodFacts
    product = await scanner_service.fetch_product_by_barcode(barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found for provided barcode.")

    # Save to database catalog
    new_prod = PackagedProduct(**product.model_dump(exclude={"id"}))
    db.add(new_prod)
    await db.commit()
    await db.refresh(new_prod)
    return ProductNutritionSchema.model_validate(new_prod)

@router.get("/search", response_model=List[ProductNutritionSchema])
async def search_packaged_products(
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    """UC-2 Search: Query packaged food by name. Checks local curated catalog first for instant English results, then supplements with OpenFoodFacts."""
    pattern = f"%{query.strip()}%"
    stmt = select(PackagedProduct).where(
        (PackagedProduct.product_name.ilike(pattern)) |
        (PackagedProduct.brand.ilike(pattern)) |
        (PackagedProduct.category.ilike(pattern))
    ).limit(10)
    res = await db.execute(stmt)
    local_prods = res.scalars().all()

    results = [ProductNutritionSchema.model_validate(p) for p in local_prods]

    # If fewer than 5 results, enrich with OpenFoodFacts external catalog
    if len(results) < 5:
        try:
            external_prods = await scanner_service.search_products_by_name(query)
            existing_names = {r.product_name.lower() for r in results}
            for ext in external_prods:
                if ext.product_name.lower() not in existing_names:
                    results.append(ext)
                    existing_names.add(ext.product_name.lower())
                    if len(results) >= 10:
                        break
        except Exception:
            pass

    return results

@router.post("/compare-alternatives", response_model=List[StatisticalComparisonSchema])
async def compare_healthy_alternatives(
    product_query: str = Form(..., description="Barcode or product name to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    UC-2 Core Service: Given any packaged food (barcode or product name),
    finds category-matched healthier alternatives and computes quantitative statistical comparisons
    (% calorie reduction, % sugar reduction, macro delta, and Nutri-Score improvement).
    """
    # 1. Resolve target original product
    original_product = None
    if product_query.isdigit():
        stmt = select(PackagedProduct).where(PackagedProduct.barcode == product_query)
        res = await db.execute(stmt)
        db_prod = res.scalar_one_or_none()
        if db_prod:
            original_product = ProductNutritionSchema.model_validate(db_prod)
        else:
            original_product = await scanner_service.fetch_product_by_barcode(product_query)

    if not original_product:
        pattern = f"%{product_query.strip()}%"
        stmt = select(PackagedProduct).where(
            (PackagedProduct.product_name.ilike(pattern)) | (PackagedProduct.brand.ilike(pattern))
        ).limit(1)
        res = await db.execute(stmt)
        db_prod = res.scalar_one_or_none()
        if db_prod:
            original_product = ProductNutritionSchema.model_validate(db_prod)
        else:
            searchResults = await scanner_service.search_products_by_name(product_query)
            if searchResults:
                original_product = searchResults[0]

    if not original_product:
        raise HTTPException(status_code=404, detail=f"Target product '{product_query}' could not be resolved.")

    # 2. Category-aware smart mapping for healthier swaps in same food group
    query_lower = (original_product.product_name + " " + (original_product.category or "")).lower()

    category_map = {
        "bread": ["whole wheat", "sourdough", "sprouted", "multigrain"],
        "chip": ["baked", "popcorn", "chickpea", "pita"],
        "cola": ["zero sugar", "sparkling", "tea"],
        "soda": ["zero sugar", "sparkling", "tea"],
        "beverage": ["sparkling", "tea", "zero sugar"],
        "drink": ["sparkling", "tea"],
        "cereal": ["oat", "granola", "wholegrain"],
        "chocolate": ["dark chocolate", "cocoa"],
        "snack": ["baked", "popcorn", "chickpea"],
        "yogurt": ["greek yogurt", "almond milk"],
        "milk": ["almond milk", "greek yogurt"],
    }

    matched_keywords = []
    for key, terms in category_map.items():
        if key in query_lower:
            matched_keywords.extend(terms)
            break

    # 3. Find candidates in database
    candidates = []
    for kw in matched_keywords:
        kw_pattern = f"%{kw}%"
        c_stmt = select(PackagedProduct).where(
            (PackagedProduct.product_name.ilike(kw_pattern))
        ).limit(3)
        c_res = await db.execute(c_stmt)
        for cp in c_res.scalars().all():
            candidates.append(ProductNutritionSchema.model_validate(cp))

    # Also check same category with lower calories
    if original_product.category:
        cat_stmt = select(PackagedProduct).where(
            (PackagedProduct.category == original_product.category) &
            (PackagedProduct.calories_100g < original_product.calories_100g)
        ).limit(5)
        cat_res = await db.execute(cat_stmt)
        for cp in cat_res.scalars().all():
            candidates.append(ProductNutritionSchema.model_validate(cp))

    # 4. Filter and build comparisons
    comparisons = []
    seen_names = set()

    for cand in candidates:
        if cand.product_name.lower() == original_product.product_name.lower():
            continue
        if cand.product_name.lower() in seen_names:
            continue
        seen_names.add(cand.product_name.lower())

        cal_diff = original_product.calories_100g - cand.calories_100g
        sugar_diff = original_product.sugar_100g - cand.sugar_100g
        protein_diff = cand.protein_100g - original_product.protein_100g
        score_diff = comparison_engine.calculate_statistical_metrics(original_product, cand).health_score_delta

        if cal_diff > 0 or sugar_diff > 0 or score_diff > 0 or protein_diff > 0:
            metrics = comparison_engine.calculate_statistical_metrics(original_product, cand)
            comparisons.append(metrics)

    # Sort alternatives by highest health score delta and calorie reduction
    comparisons.sort(key=lambda x: (x.health_score_delta, x.calorie_reduction_pct), reverse=True)
    return comparisons[:5]
