from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    meal_logs = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")
    saved_collections = relationship("UserSavedCollection", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    weight_kg = Column(Float, nullable=True)
    height_cm = Column(Float, nullable=True)
    activity_level = Column(String(50), default="moderately_active") # sedentary, moderately_active, active
    primary_goal = Column(String(50), default="maintenance") # weight_loss, muscle_gain, maintenance
    dietary_preference = Column(String(50), default="any") # vegetarian, vegan, keto, any
    target_daily_calories = Column(Integer, default=2000)
    target_protein_g = Column(Integer, default=150)
    target_carbs_g = Column(Integer, default=200)
    target_fat_g = Column(Integer, default=65)

    user = relationship("User", back_populates="profile")
