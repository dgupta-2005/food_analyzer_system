from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from app.schemas.product import ProductNutritionSchema

class RecommendedDish(BaseModel):
    dish_name: str
    portion_size: str
    target_calories: float
    protein_g: float
    carbs_g: float
    fats_g: float
    reason: str

class DailyMealSlot(BaseModel):
    slot_name: str # e.g. Breakfast, Lunch, Evening Snack, Dinner
    target_calories: float
    recommended_dishes: List[RecommendedDish]
    healthy_packaged_products: List[ProductNutritionSchema] = []

class MealPlanResponse(BaseModel):
    plan_title: str
    target_daily_calories: int
    user_goal: str
    daily_slots: List[DailyMealSlot]
    overall_advice: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
