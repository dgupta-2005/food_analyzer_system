from pydantic import BaseModel, Field
from typing import Optional, List

class ProductNutritionSchema(BaseModel):
    id: Optional[int] = None
    barcode: Optional[str] = None
    product_name: str
    brand: Optional[str] = "Unknown"
    category: Optional[str] = "General"
    image_url: Optional[str] = None
    serving_size_g: float = 100.0
    calories_100g: float = 0.0
    protein_100g: float = 0.0
    carbs_100g: float = 0.0
    fat_100g: float = 0.0
    sugar_100g: float = 0.0
    sodium_mg_100g: float = 0.0
    nutri_score: Optional[str] = None # A, B, C, D, E

    class Config:
        from_attributes = True

class BarcodeScanResponse(BaseModel):
    barcode: Optional[str]
    success: bool
    message: str
    product: Optional[ProductNutritionSchema] = None

class StatisticalComparisonSchema(BaseModel):
    original_product: ProductNutritionSchema
    alternative_product: ProductNutritionSchema
    calorie_reduction_pct: float
    sugar_reduction_pct: float
    protein_increase_pct: float
    health_score_delta: float
    summary_verdict: str
