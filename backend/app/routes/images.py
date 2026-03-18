from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.image import Image

router = APIRouter()

@router.get("/")
def get_images(db: Session = Depends(get_db)):
    images = db.query(Image).limit(1000).all()
    return images