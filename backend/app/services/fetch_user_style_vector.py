from app.models.user_style_vector import UserStyleVector
from sqlalchemy.orm import Session

def get_user_style_vector(db: Session, user_id: int):
    user_style_row = (
        db.query(UserStyleVector)
        .filter(UserStyleVector.user_id == user_id)
        .first()
    )

    if not user_style_row:
        raise ValueError(f"user_style_vector not found for user_id {user_id}")

    return {
        "user_id": user_style_row.user_id,
        "source_item_count": user_style_row.source_item_count,
        "style_vector": user_style_row.style_vector,
    }