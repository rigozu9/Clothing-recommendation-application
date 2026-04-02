from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from app.db import get_db
from app.models.app_user import AppUser
from app.schemas import UserCreate, UserOut, UserLogin

router = APIRouter()


@router.post("/register", response_model=UserOut)
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

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(AppUser).filter(AppUser.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not bcrypt.checkpw(payload.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "user_id": user.id,
        "username": user.username,
    }