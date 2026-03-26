from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.recommendation_service import get_recommendations_for_user

router = APIRouter()

@router.get("/{user_id}")
def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_recommendations_for_user(db=db, user_id=user_id, top_k=10)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))