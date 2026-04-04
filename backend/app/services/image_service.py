from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.models.image import Image
from app.models.image_gender import ImageGender


def get_images_for_swiping(db: Session, gender_mode: str = "all", limit: int = 1000):
    query = (
        db.query(Image)
        .join(
            ImageGender,
            (Image.image_id == ImageGender.image_id) &
            (Image.split == ImageGender.split)
        )
    )

    if gender_mode == "female":
        query = query.filter(
            or_(
                ImageGender.genders.any("Female"),
                ImageGender.genders.any("Neutral")
            )
        )

    elif gender_mode == "male":
        query = query.filter(
            ImageGender.genders.any("Male")
        )

    return query.order_by(func.random()).limit(limit).all()