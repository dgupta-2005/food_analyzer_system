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
async def search_packaged_products(query: str = Query(..., min_length=2)):
    """UC-2 Search: Query packaged food by company name, brand, or product title."""
    results = await scanner_service.search_products_by_name(query)
    return results

@router.post("/compare-alternatives", response_model=List[StatisticalComparisonSchema])
async def compare_healthy_alternatives(
    product_query: str = Form(..., description="Barcode or product name to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """
    UC-2 Core Service: Given any packaged food (barcode or product name),
    finds healthier alternatives in the catalog and computes quantitative statistical comparisons
    (% calorie reduction, % sugar reduction, macro delta, and Nutri-Score improvement).
    """
    # 1. Resolve target original product
    original_product = None
    if product_query.isdigit():
        original_product = await scanner_service.fetch_product_by_barcode(product_query)

    if not original_product:
        searchResults = await scanner_service.search_products_by_name(product_query)
        if searchResults:
            original_product = searchResults[0]

    if not original_product:
        raise HTTPException(status_code=404, detail=f"Target product '{product_query}' could not be resolved.")

    # 2. Search candidate alternatives with superior health profile in same category
    category_search = original_product.category or "healthy snacks"
    candidates = await scanner_service.search_products_by_name(f"organic {category_search}")

    if not candidates:
        # Fallback search for healthy items
        candidates = await scanner_service.search_products_by_name("oats dark chocolate almonds")

    comparisons = []
    for cand in candidates:
        # Filter items with lower calories or lower sugar
        if cand.calories_100g < original_product.calories_100g or cand.sugar_100g < original_product.sugar_100g:
            metrics = comparison_engine.calculate_statistical_metrics(original_product, cand)
            comparisons.append(metrics)

    # Sort alternatives by highest health score delta and calorie reduction
    comparisons.sort(key=lambda x: (x.health_score_delta, x.calorie_reduction_pct), reverse=True)
    return comparisons[:5]
