import cv2
import zxingcpp
import httpx
from typing import Optional, List
from app.schemas.product import ProductNutritionSchema, BarcodeScanResponse

class ProductScannerService:
    def scan_barcode_from_image_path(self, image_path: str) -> Optional[str]:
        """Reads image file and decodes barcode using zxingcpp with preprocessing fallback."""
        image = cv2.imread(image_path)
        if image is None:
            return None

        # 1. Direct detection
        results = zxingcpp.read_barcodes(image)
        if results and results[0].text.strip():
            return results[0].text.strip()

        # 2. Preprocessing: Crop quiet noise & pad white border
        h, w = image.shape[:2]
        crop = image[:, int(w * 0.05):]
        padded = cv2.copyMakeBorder(crop, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        results = zxingcpp.read_barcodes(padded)
        if results and results[0].text.strip():
            return results[0].text.strip()

        return None

    async def fetch_product_by_barcode(self, barcode: str) -> Optional[ProductNutritionSchema]:
        """Queries OpenFoodFacts database API v2 by barcode string."""
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        headers = {"User-Agent": "FoodLensApp - FastAPI Backend - Version 1.0"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
                if response.status_code != 200:
                    return None

                payload = response.json()
                if payload.get("status") != 1:
                    return None

                product = payload.get("product", {})
                nutriments = product.get("nutriments", {})

                return ProductNutritionSchema(
                    barcode=barcode,
                    product_name=product.get("product_name", "Unknown Product"),
                    brand=product.get("brands", "Unknown"),
                    category=product.get("categories", "General").split(",")[0] if product.get("categories") else "General",
                    image_url=product.get("image_front_url") or product.get("image_url"),
                    serving_size_g=float(product.get("serving_quantity", 100.0) or 100.0),
                    calories_100g=float(nutriments.get("energy-kcal_100g", 0.0) or 0.0),
                    protein_100g=float(nutriments.get("proteins_100g", 0.0) or 0.0),
                    carbs_100g=float(nutriments.get("carbohydrates_100g", 0.0) or 0.0),
                    fat_100g=float(nutriments.get("fat_100g", 0.0) or 0.0),
                    sugar_100g=float(nutriments.get("sugars_100g", 0.0) or 0.0),
                    sodium_mg_100g=float(nutriments.get("sodium_100g", 0.0) or 0.0) * 1000.0,
                    nutri_score=product.get("nutriscore_grade", "c").upper() if product.get("nutriscore_grade") else "C"
                )
            except Exception as e:
                print(f"⚠️ OpenFoodFacts API error: {e}")
                return None

    async def search_products_by_name(self, query: str) -> List[ProductNutritionSchema]:
        """Searches OpenFoodFacts by product/brand name query string with English preference."""
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&action=process&json=1&page_size=12&lc=en"
        headers = {"User-Agent": "FoodLensApp - FastAPI Backend - Version 1.0 (dev@foodlens.org)"}

        async with httpx.AsyncClient(timeout=8.0) as client:
            try:
                response = await client.get(url, headers=headers)
                if response.status_code != 200:
                    return []

                data = response.json()
                products_raw = data.get("products", [])
                results = []

                for item in products_raw:
                    nutriments = item.get("nutriments", {})
                    # Prioritize English title if present
                    name = item.get("product_name_en") or item.get("product_name")
                    if not name:
                        continue

                    results.append(ProductNutritionSchema(
                        barcode=item.get("code"),
                        product_name=name,
                        brand=item.get("brands", "Unknown"),
                        category=item.get("categories", "General").split(",")[0] if item.get("categories") else "General",
                        image_url=item.get("image_front_small_url") or item.get("image_url"),
                        calories_100g=float(nutriments.get("energy-kcal_100g", 0.0) or 0.0),
                        protein_100g=float(nutriments.get("proteins_100g", 0.0) or 0.0),
                        carbs_100g=float(nutriments.get("carbohydrates_100g", 0.0) or 0.0),
                        fat_100g=float(nutriments.get("fat_100g", 0.0) or 0.0),
                        sugar_100g=float(nutriments.get("sugars_100g", 0.0) or 0.0),
                        sodium_mg_100g=float(nutriments.get("sodium_100g", 0.0) or 0.0) * 1000.0,
                        nutri_score=item.get("nutriscore_grade", "c").upper() if item.get("nutriscore_grade") else "C"
                    ))
                return results
            except Exception as e:
                print(f"[WARN] OpenFoodFacts Search error: {e}")
                return []

scanner_service = ProductScannerService()
