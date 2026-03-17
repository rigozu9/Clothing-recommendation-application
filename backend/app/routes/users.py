from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from app.db import get_db
from app.models import AppUser
from app.schemas import UserCreate, UserOut

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(AppUser).filter(AppUser.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    password_hash = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()

    user = AppUser(
        username=payload.username,
        password_hash=password_hash
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user