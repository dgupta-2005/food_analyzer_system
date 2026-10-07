from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: Optional[str] = None

class UserProfileCreate(BaseModel):
    age: Optional[int] = Field(default=25, ge=1, le=120)
    gender: Optional[str] = "other"
    weight_kg: Optional[float] = Field(default=70.0, ge=20.0, le=300.0)
    height_cm: Optional[float] = Field(default=170.0, ge=50.0, le=250.0)
    activity_level: Optional[str] = "moderately_active"
    primary_goal: Optional[str] = "maintenance"
    dietary_preference: Optional[str] = "any"
    target_daily_calories: int = Field(default=2000, ge=800, le=6000)
    target_protein_g: int = Field(default=150, ge=0)
    target_carbs_g: int = Field(default=200, ge=0)
    target_fat_g: int = Field(default=65, ge=0)

class UserProfileResponse(UserProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True
