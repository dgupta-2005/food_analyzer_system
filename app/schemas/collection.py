from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.product import ProductNutritionSchema

class CollectionSaveRequest(BaseModel):
    user_id: int
    product_id: int
    tag: str = Field(default="Favorites")
    user_notes: Optional[str] = None

class CollectionItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    tag: str
    user_notes: Optional[str] = None
    saved_at: datetime
    product: ProductNutritionSchema

    class Config:
        from_attributes = True
