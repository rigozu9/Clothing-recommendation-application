from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from app.db import Base


class ImageGender(Base):
    __tablename__ = "int_imat_image_gender"
    __table_args__ = {"schema": "analytics"}

    split = Column(String, primary_key=True)
    image_id = Column(Integer, primary_key=True)
    genders = Column(ARRAY(String))