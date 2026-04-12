from sqlalchemy import Column, Integer, String, Index
from app.db import Base

class MartImage(Base):
    __tablename__ = "mart_images"
    __table_args__ = (
        Index("ix_mart_images_swipe_gender_mode", "swipe_gender_mode"),
        Index("ix_mart_images_gender_image_id", "swipe_gender_mode", "image_id"),
        {"schema": "analytics"},
    )

    image_id = Column(Integer, primary_key=True, index=True)
    split = Column(String, primary_key=True)
    url = Column(String)
    swipe_gender_mode = Column(String)