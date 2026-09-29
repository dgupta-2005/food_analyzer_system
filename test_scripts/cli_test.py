import os
import json
from abc import ABC, abstractmethod
from typing import Optional

import cv2
import zxingcpp
import httpx
from dotenv import load_dotenv
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

# ==========================================
# 1. DOMAIN MODELS (Strict Typing)
# ==========================================

class MacroNutrients(BaseModel):
    item_name: str = Field(description="Name or summary of the food item")
    calories: float = Field(ge=0, description="Estimated total calories (kcal)")
    protein_g: float = Field(ge=0, description="Protein in grams")
    carbs_g: float = Field(ge=0, description="Carbohydrates in grams")
    fats_g: float = Field(ge=0, description="Fats in grams")
    confidence_score: float = Field(
        ge=0.0, le=1.0, description="Estimation confidence between 0.0 and 1.0"
    )

class ProductNutrition(BaseModel):
    barcode: str
    product_name: str
    brand: Optional[str] = "Unknown"
    calories_100g: float = 0.0
    protein_100g: float = 0.0
    carbs_100g: float = 0.0
    fat_100g: float = 0.0
    sugar_100g: float = 0.0

# ==========================================
# 2. INTERFACES (Dependency Inversion)
# ==========================================

class IProductScanner(ABC):
    @abstractmethod
    def scan_barcode(self, image_path: str) -> Optional[str]:
        pass

    @abstractmethod
    def fetch_product_details(self, barcode: str) -> Optional[ProductNutrition]:
        pass

class IMealEstimator(ABC):
    @abstractmethod
    def estimate_meal(
        self, image_path: Optional[str], description: Optional[str]
    ) -> MacroNutrients:
        pass

# ==========================================
# 3. CONCRETE IMPLEMENTATIONS
# ==========================================

class OpenFoodFactsScanner(IProductScanner):
    """Decodes barcodes using zxingcpp and queries OpenFoodFacts."""

    def scan_barcode(self, image_path: str) -> Optional[str]:
        image = cv2.imread(image_path)
        if image is None:
            return None

        # 1. Try decoding raw image first
        results = zxingcpp.read_barcodes(image)
        if results and results[0].text.strip():
            return results[0].text.strip()

        # 2. Preprocess: Crop noise edge and add white quiet zone
        h, w = image.shape[:2]
        crop = image[:, int(w * 0.05):]
        padded = cv2.copyMakeBorder(crop, 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        
        results = zxingcpp.read_barcodes(padded)
        if results and results[0].text.strip():
            return results[0].text.strip()

        return None

    def fetch_product_details(self, barcode: str) -> Optional[ProductNutrition]:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        headers = {"User-Agent": "FoodLensApp - CLIPrototype - Version 1.0"}

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                return None

            payload = response.json()
            if payload.get("status") != 1:
                return None

            product = payload.get("product", {})
            nutriments = product.get("nutriments", {})

            return ProductNutrition(
                barcode=barcode,
                product_name=product.get("product_name", "Unknown Product"),
                brand=product.get("brands", "Unknown"),
                calories_100g=float(nutriments.get("energy-kcal_100g", 0.0) or 0.0),
                protein_100g=float(nutriments.get("proteins_100g", 0.0) or 0.0),
                carbs_100g=float(nutriments.get("carbohydrates_100g", 0.0) or 0.0),
                fat_100g=float(nutriments.get("fat_100g", 0.0) or 0.0),
                sugar_100g=float(nutriments.get("sugars_100g", 0.0) or 0.0),
            )

class GeminiMealEstimator(IMealEstimator):
    """Uses Google GenAI SDK with structured output enforcement."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        self.client = genai.Client(api_key=api_key)

    def estimate_meal(
        self, image_path: Optional[str], description: Optional[str]
    ) -> MacroNutrients:
        contents = []

        system_instruction = (
            "You are an expert clinical dietitian and food portion specialist. "
            "Analyze the meal from the provided image and/or text description. "
            "Provide realistic macro counts and caloric estimates. "
            f"User portion notes: {description or 'None provided.'}"
        )
        contents.append(system_instruction)

        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            contents.append(img)

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MacroNutrients,
                temperature=0.2,
            ),
        )

        return MacroNutrients.model_validate_json(response.text)

# ==========================================
# 4. TERMINAL CLI RUNNER
# ==========================================

def run_cli():
    print("=" * 60)
    print("🥗 NUTRITION & PACKAGED FOOD ENGINE (TERMINAL PROTOTYPE)")
    print("=" * 60)

    scanner = OpenFoodFactsScanner()
    estimator = GeminiMealEstimator()

    while True:
        print("\nAvailable Operations:")
        print("1. Estimate Meal Calories (via text or image path)")
        print("2. Scan Barcode Image (zxingcpp + OpenFoodFacts)")
        print("3. Lookup Barcode Number Directly")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            img_path = input("Enter meal image path (leave blank if none): ").strip()
            desc = input("Enter meal description/portions: ").strip()

            clean_img = img_path if (img_path and os.path.exists(img_path)) else None
            if not clean_img and not desc:
                print("❌ Provide at least a description or a valid image path.")
                continue

            print("\n⏳ Processing estimation with Gemini...")
            try:
                result = estimator.estimate_meal(clean_img, desc)
                print("\n✅ Caloric Breakdown:")
                print(json.dumps(result.model_dump(), indent=2))
            except Exception as e:
                print(f"❌ Failed to estimate meal: {e}")

        elif choice == "2":
            img_path = input("Enter path to barcode image: ").strip()
            if not os.path.exists(img_path):
                print("❌ File path does not exist.")
                continue

            print("⏳ Scanning image with zxingcpp...")
            barcode = scanner.scan_barcode(img_path)
            if not barcode:
                print("❌ No barcode pattern found in the image.")
                continue

            print(f" Detected barcode: {barcode}")
            print("⏳ Querying OpenFoodFacts...")
            product = scanner.fetch_product_details(barcode)
            if product:
                print("\n✅ Product Found:")
                print(json.dumps(product.model_dump(), indent=2))
            else:
                print("❌ Product not found in database.")

        elif choice == "3":
            code = input("Enter barcode number directly (e.g. 5449000000996): ").strip()
            print("⏳ Querying OpenFoodFacts...")
            product = scanner.fetch_product_details(code)
            if product:
                print("\n✅ Product Found:")
                print(json.dumps(product.model_dump(), indent=2))
            else:
                print("❌ Product not found.")

        elif choice == "4":
            print("Terminating CLI.")
            break
        else:
            print("Invalid input. Select between 1 and 4.")

if __name__ == "__main__":
    run_cli()