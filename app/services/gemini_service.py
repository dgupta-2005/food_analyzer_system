import os
import time
from typing import Optional, List
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from app.core.config import settings
from app.schemas.meal import MacroNutrientItem

class AIStructuredMealResponse(BaseModel):
    summary_item_name: str = Field(description="Brief summary or dish name of the meal")
    total_calories: float = Field(ge=0, description="Total estimated calories")
    total_protein_g: float = Field(ge=0, description="Total protein in grams")
    total_carbs_g: float = Field(ge=0, description="Total carbs in grams")
    total_fats_g: float = Field(ge=0, description="Total fats in grams")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence rating between 0.0 and 1.0")
    items: List[MacroNutrientItem] = Field(description="Breakdown of individual food components in the meal")

MODEL_FALLBACKS = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]

class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment.")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def estimate_meal(
        self, image_path: Optional[str] = None, description: Optional[str] = None
    ) -> AIStructuredMealResponse:
        """Estimates caloric and macronutrient values from an image and/or text description with fallback models."""
        contents = []

        system_prompt = (
            "You are an expert clinical dietitian, nutritionist, and portion estimator. "
            "Analyze the meal provided via the image and/or text description. "
            "Provide an accurate, realistic breakdown of all dishes/components, their portion sizes, "
            "calories, protein, carbohydrates, and fats. "
            f"User portion notes / context: {description or 'None provided.'}"
        )
        contents.append(system_prompt)

        if image_path and os.path.exists(image_path):
            img = Image.open(image_path)
            contents.append(img)

        last_exception = None

        for model_name in MODEL_FALLBACKS:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=AIStructuredMealResponse,
                        temperature=0.2,
                    ),
                )
                return AIStructuredMealResponse.model_validate_json(response.text)
            except Exception as e:
                print(f"⚠️ Model '{model_name}' temporary error: {e}. Trying fallback...")
                last_exception = e
                time.sleep(1)

        raise RuntimeError(f"All Gemini models failed. Last error: {last_exception}")

gemini_service = GeminiService()
