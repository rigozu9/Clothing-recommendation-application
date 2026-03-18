from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY, DOUBLE_PRECISION
from sqlalchemy.orm import relationship

from app.db import Base


class UserStyleVector(Base):
    __tablename__ = "user_style_vector"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("analytics.app_user.id", ondelete="CASCADE"), nullable=False)
    style_vector = Column(ARRAY(DOUBLE_PRECISION), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("AppUser", back_populates="style_vectors")