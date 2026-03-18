from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db import Base


class AppUser(Base):
    __tablename__ = "app_user"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    style_vectors = relationship("UserStyleVector", back_populates="user", cascade="all, delete")