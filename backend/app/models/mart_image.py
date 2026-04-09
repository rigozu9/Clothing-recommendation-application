from sqlalchemy import Column, Integer, String
from app.db import Base

class MartImage(Base):
    __tablename__ = "mart_images"
    __table_args__ = {"schema": "analytics"}

    image_id = Column(Integer, primary_key=True, index=True)
    split = Column(String, primary_key=True)
    url = Column(String)
    swipe_gender_mode = Column(String)