from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.mart_image import MartImage

def get_images_for_swiping(db: Session, gender_mode: str = "all", limit: int = 1000):
    query = db.query(MartImage)

    if gender_mode in ["male", "female"]:
        query = query.filter(MartImage.swipe_gender_mode == gender_mode)

    return query.order_by(func.random()).limit(limit).all()