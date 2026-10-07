import asyncio
import os
import sys
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent

from app.core.config import settings

async def test_backend():
    print("[TEST] Running Backend Integration Test...")
    
    # 1. Test Config & Gemini Key
    print(f"[OK] Project Name: {settings.PROJECT_NAME}")
    print(f"[OK] Gemini Key Loaded: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
    
    # 2. Test OpenFoodFacts Barcode Scanner API
    from app.services.scanner_service import scanner_service
    test_barcode = "5449000000996" # Coca Cola barcode
    prod = await scanner_service.fetch_product_by_barcode(test_barcode)
    if prod:
        print(f"[OK] OpenFoodFacts Integration: Found '{prod.product_name}' ({prod.calories_100g} kcal/100g)")
    else:
        print("[FAIL] OpenFoodFacts query failed")

    # 3. Test Health Comparison Engine
    from app.services.comparison_service import comparison_engine
    from app.schemas.product import ProductNutritionSchema
    orig = ProductNutritionSchema(product_name="Fried Chips", calories_100g=536, sugar_100g=5.0, protein_100g=7.0, nutri_score="E")
    alt = ProductNutritionSchema(product_name="Baked Oats Chips", calories_100g=380, sugar_100g=1.2, protein_100g=12.0, nutri_score="A")
    comp = comparison_engine.calculate_statistical_metrics(orig, alt)
    print(f"[OK] Statistical Metrics Delta: {comp.calorie_reduction_pct}% Calorie Reduction")
    print(f"     Verdict: {comp.summary_verdict}")

    # 4. Test Recommendation Engine
    from app.services.recommendation_service import recommendation_service
    from app.schemas.user import UserProfileResponse
    prof = UserProfileResponse(id=1, user_id=1, primary_goal="weight_loss", target_daily_calories=1800)
    plan = recommendation_service.generate_personalized_plan(prof, [])
    print(f"[OK] Recommendation Engine: Generated '{plan.plan_title}' with {len(plan.daily_slots)} meal slots.")

    # 5. Test Gemini Meal Estimation with local test image
    from app.services.gemini_service import gemini_service
    test_image_path = os.path.join(ROOT_DIR, "Overnight-Oats-3.jpg")
    if os.path.exists(test_image_path):
        print(f"[TEST] Testing Gemini Vision AI with '{test_image_path}'...")
        res = gemini_service.estimate_meal(image_path=test_image_path, description="Overnight oats with fruit")
        print(f"[OK] Gemini Vision Result: Dish='{res.summary_item_name}', Calories={res.total_calories} kcal, Protein={res.total_protein_g}g")
        for item in res.items:
            print(f"     - Item: {item.item_name} ({item.calories} kcal, {item.protein_g}g protein)")

if __name__ == "__main__":
    asyncio.run(test_backend())
