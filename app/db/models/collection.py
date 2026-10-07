from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserSavedCollection(Base):
    __tablename__ = "user_saved_collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("packaged_products.id", ondelete="CASCADE"), nullable=False)
    tag = Column(String(50), default="Favorites", index=True)
    user_notes = Column(Text, nullable=True)
    saved_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_user_product"),
    )

    user = relationship("User", back_populates="saved_collections")
    product = relationship("PackagedProduct", back_populates="saved_entries")
