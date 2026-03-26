from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user_style_vector import UserStyleVector
from app.services.user_style_vector_service import get_user_style_vector
from app.schemas import UserStyleVectorCreate, UserStyleVectorOut

router = APIRouter()


@router.post("/", response_model=UserStyleVectorOut)
def create_user_style_vector(payload: UserStyleVectorCreate, db: Session = Depends(get_db)):
    row = UserStyleVector(
        user_id=payload.user_id,
        style_vector=payload.style_vector
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/{user_id}")
def read_user_style_vector(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_user_style_vector(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))