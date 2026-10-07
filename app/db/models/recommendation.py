from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_title = Column(String(150), nullable=False)
    target_calories = Column(Integer, nullable=False)
    plan_data = Column(JSON, nullable=False) # JSON payload containing daily structure
    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="meal_plans")
