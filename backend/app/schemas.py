from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class LikeItemRequest(BaseModel):
    image_id: int

class UserStyleVectorCreate(BaseModel):
    user_id: int
    style_vector: List[float]


class UserStyleVectorOut(BaseModel):
    id: int
    user_id: int
    style_vector: List[float]

    class Config:
        from_attributes = True