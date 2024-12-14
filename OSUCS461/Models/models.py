from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserWriteModel(BaseModel):
    username: str
    email: EmailStr

class UserReadModel(UserWriteModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserPostWriteModel(BaseModel):
    user_id: int
    content: str

class UserPostReadModel(UserPostWriteModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
