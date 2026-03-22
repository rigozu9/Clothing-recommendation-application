from sqlalchemy import Column, Integer, BigInteger, TIMESTAMP, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.db import Base


class UserLikedItem(Base):
    __tablename__ = "user_liked_item"
    __table_args__ = (
        UniqueConstraint("user_id", "image_id", name="uq_user_liked_item_user_image"),
        {"schema": "analytics"},
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("analytics.app_user.id", ondelete="CASCADE"),
        nullable=False,
    )
    image_id = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("AppUser", back_populates="liked_items")