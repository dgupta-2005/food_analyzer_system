from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class PackagedProduct(Base):
    __tablename__ = "packaged_products"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(64), unique=True, index=True, nullable=True)
    product_name = Column(String(255), index=True, nullable=False)
    brand = Column(String(150), index=True, nullable=True, default="Unknown")
    category = Column(String(100), index=True, nullable=True, default="General")
    image_url = Column(String(512), nullable=True)
    serving_size_g = Column(Float, default=100.0)
    calories_100g = Column(Float, nullable=False, default=0.0)
    protein_100g = Column(Float, nullable=False, default=0.0)
    carbs_100g = Column(Float, nullable=False, default=0.0)
    fat_100g = Column(Float, nullable=False, default=0.0)
    sugar_100g = Column(Float, nullable=False, default=0.0)
    sodium_mg_100g = Column(Float, nullable=False, default=0.0)
    nutri_score = Column(String(2), nullable=True) # A, B, C, D, E
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    saved_entries = relationship("UserSavedCollection", back_populates="product", cascade="all, delete-orphan")


class StatisticalComparison(Base):
    __tablename__ = "statistical_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    original_product_id = Column(Integer, ForeignKey("packaged_products.id", ondelete="CASCADE"), nullable=False)
    alternative_product_id = Column(Integer, ForeignKey("packaged_products.id", ondelete="CASCADE"), nullable=False)
    calorie_reduction_pct = Column(Float, nullable=False, default=0.0)
    sugar_reduction_pct = Column(Float, nullable=False, default=0.0)
    protein_increase_pct = Column(Float, nullable=False, default=0.0)
    health_score_delta = Column(Float, nullable=False, default=0.0)
    ai_verdict = Column(Text, nullable=True)

    original_product = relationship("PackagedProduct", foreign_keys=[original_product_id])
    alternative_product = relationship("PackagedProduct", foreign_keys=[alternative_product_id])
