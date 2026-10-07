from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MacroNutrientItem(BaseModel):
    item_name: str = Field(description="Name of the food item or dish portion")
    portion_description: Optional[str] = Field(default="1 serving", description="Quantified portion size")
    calories: float = Field(ge=0, description="Estimated calories in kcal")
    protein_g: float = Field(ge=0, description="Protein in grams")
    carbs_g: float = Field(ge=0, description="Carbohydrates in grams")
    fats_g: float = Field(ge=0, description="Fats in grams")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)

class MealEstimationResponse(BaseModel):
    summary_item_name: str
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float
    confidence_score: float
    image_url: Optional[str] = None
    items: List[MacroNutrientItem]

class MealLogCreate(BaseModel):
    user_id: int
    image_url: Optional[str] = None
    user_description: Optional[str] = None
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float
    items: List[MacroNutrientItem]

class MealItemResponse(MacroNutrientItem):
    id: int
    meal_log_id: int

    class Config:
        from_attributes = True

class MealLogResponse(BaseModel):
    id: int
    user_id: int
    image_url: Optional[str] = None
    user_description: Optional[str] = None
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float
    logged_at: datetime
    items: List[MealItemResponse] = []

    class Config:
        from_attributes = True
