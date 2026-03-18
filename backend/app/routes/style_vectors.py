from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user_style_vector import UserStyleVector
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


@router.get("/latest/{user_id}", response_model=UserStyleVectorOut)
def get_latest_user_style_vector(user_id: int, db: Session = Depends(get_db)):
    row = (
        db.query(UserStyleVector)
        .filter(UserStyleVector.user_id == user_id)
        .order_by(UserStyleVector.created_at.desc(), UserStyleVector.id.desc())
        .first()
    )
    return row