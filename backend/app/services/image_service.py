from sqlalchemy.orm import Session
from sqlalchemy import func, or_, cast
from sqlalchemy.dialects.postgresql import ARRAY, TEXT

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
                ImageGender.genders.contains(cast(["Female"], ARRAY(TEXT))),
                ImageGender.genders.contains(cast(["Neutral"], ARRAY(TEXT)))
            )
        )

    elif gender_mode == "male":
        query = query.filter(
            ImageGender.genders.contains(
                cast(["Male"], ARRAY(TEXT))
            )
        )

    return query.order_by(func.random()).limit(limit).all()