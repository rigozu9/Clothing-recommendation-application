from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.image_service import get_images_for_swiping

router = APIRouter()

@router.get("/")
def get_images(
    gender_mode: str = Query("all"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return get_images_for_swiping(db=db, gender_mode=gender_mode, limit=limit)