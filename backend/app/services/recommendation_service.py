import numpy as np
from sqlalchemy.orm import Session

from app.models.user_style_vector import UserStyleVector
from app.models.user_liked_item import UserLikedItem
from app.ml.artifacts import index_df, X, nn_model


def get_recommendations_for_user(db: Session, user_id: int, top_k: int = 10):
    user_style_row = (
        db.query(UserStyleVector)
        .filter(UserStyleVector.user_id == user_id)
        .first()
    )

    if not user_style_row:
        raise ValueError(f"user_style_vector not found for user_id {user_id}")

    user_vector = np.array(user_style_row.style_vector, dtype=float)

    if user_vector.shape[0] != X.shape[1]:
        raise ValueError(
            f"user vector length {user_vector.shape[0]} does not match item matrix width {X.shape[1]}"
        )

    user_vector_2d = user_vector.reshape(1, -1)

    liked_image_ids = {
        row.image_id
        for row in db.query(UserLikedItem).filter(UserLikedItem.user_id == user_id).all()
    }

    distances, indices = nn_model.kneighbors(user_vector_2d, n_neighbors=top_k + len(liked_image_ids))

    neighbor_rows = indices[0]
    neighbor_distances = distances[0]

    result = index_df.iloc[neighbor_rows].copy()
    result["distance"] = neighbor_distances
    result["similarity"] = 1 - result["distance"]

    if liked_image_ids:
        # Remove items the user has already liked:
        # - result["image_id"].isin(liked_image_ids) → True for liked items
        # - ~ (NOT) flips it → True for items NOT liked
        # - result[...] keeps only those rows
        result = result[~result["image_id"].isin(liked_image_ids)]

    result = result.head(top_k)

    return {
        "user_id": user_id,
        "source_item_count": user_style_row.source_item_count,
        "recommendations": [
            {
                "image_id": int(row.image_id),
                "similarity": float(row.similarity),
            }
            for row in result.itertuples(index=False)
        ],
    }