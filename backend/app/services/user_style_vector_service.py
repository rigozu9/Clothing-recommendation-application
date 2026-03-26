import numpy as np
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_liked_item import UserLikedItem
from app.models.user_style_vector import UserStyleVector
from app.ml.artifacts import index_df, X
from app.ml.vector_utils import get_item_vector


def update_user_vector_incrementally(old_vector, old_count, item_vector):
    old_vector = np.array(old_vector, dtype=float)
    item_vector = np.array(item_vector, dtype=float)

    if old_count == 0:
        return item_vector.tolist(), 1

    new_vector = (old_vector * old_count + item_vector) / (old_count + 1)
    return new_vector.tolist(), old_count + 1


def add_like_and_update_user_vector(db: Session, user_id: int, image_id: int):
    liked_item = UserLikedItem(user_id=user_id, image_id=image_id)
    db.add(liked_item)

    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise ValueError(f"user {user_id} already liked image {image_id}")

    user_style_row = (
        db.query(UserStyleVector)
        .filter(UserStyleVector.user_id == user_id)
        .first()
    )

    if not user_style_row:
        raise ValueError(f"user_style_vector not found for user_id {user_id}")

    item_vector = get_item_vector(image_id=image_id, index_df=index_df, X=X)

    if len(item_vector) != len(user_style_row.style_vector):
        raise ValueError(
            f"vector size mismatch: item vector has length {len(item_vector)}, "
            f"user vector has length {len(user_style_row.style_vector)}"
        )

    new_vector, new_count = update_user_vector_incrementally(
        old_vector=user_style_row.style_vector,
        old_count=user_style_row.source_item_count,
        item_vector=item_vector,
    )

    user_style_row.style_vector = new_vector
    user_style_row.source_item_count = new_count

    db.commit()
    db.refresh(user_style_row)

    return {
        "user_id": user_id,
        "image_id": image_id,
        "source_item_count": user_style_row.source_item_count,
        "style_vector": user_style_row.style_vector,
    }

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