from sqlalchemy import Column, Integer, String

from app.db import Base


class Image(Base):
    __tablename__ = "stg_imat_images"
    __table_args__ = {"schema": "analytics_stg"}

    image_id = Column(Integer, primary_key=True, index=True)
    split = Column(String)
    url = Column(String)