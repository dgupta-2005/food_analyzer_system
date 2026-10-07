from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(512), nullable=True)
    user_description = Column(Text, nullable=True)
    total_calories = Column(Float, nullable=False, default=0.0)
    total_protein_g = Column(Float, nullable=False, default=0.0)
    total_carbs_g = Column(Float, nullable=False, default=0.0)
    total_fats_g = Column(Float, nullable=False, default=0.0)
    logged_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="meal_logs")
    items = relationship("MealItem", back_populates="meal_log", cascade="all, delete-orphan")


class MealItem(Base):
    __tablename__ = "meal_items"

    id = Column(Integer, primary_key=True, index=True)
    meal_log_id = Column(Integer, ForeignKey("meal_logs.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(150), nullable=False)
    portion_description = Column(String(100), nullable=True)
    calories = Column(Float, nullable=False, default=0.0)
    protein_g = Column(Float, nullable=False, default=0.0)
    carbs_g = Column(Float, nullable=False, default=0.0)
    fats_g = Column(Float, nullable=False, default=0.0)
    confidence_score = Column(Float, default=1.0)

    meal_log = relationship("MealLog", back_populates="items")
