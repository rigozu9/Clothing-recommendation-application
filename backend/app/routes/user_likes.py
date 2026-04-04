from fastapi import APIRouter, Depends, HTTPException
from app.schemas import LikeItemRequest
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.user_style_vector_service import add_like_and_update_user_vector

router = APIRouter()

@router.post("/{user_id}/like")
def like_item(user_id: int, payload: LikeItemRequest, db: Session = Depends(get_db)):
    try:
        result = add_like_and_update_user_vector(
            db=db,
            user_id=user_id,
            image_id=payload.image_id,
        )
        return result

    except ValueError as e:
        print(
            f"LIKE ERROR | user_id={user_id} | image_id={payload.image_id} | error={str(e)}"
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print(
            f"UNEXPECTED LIKE ERROR | user_id={user_id} | image_id={payload.image_id} | error={str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")