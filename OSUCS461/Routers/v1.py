from fastapi import APIRouter, HTTPException
from Classes.Database.logic import User, UserPost
from Models.models import UserWriteModel, UserReadModel, UserPostWriteModel, UserPostReadModel
from typing import List

router = APIRouter()

@router.post("/users", response_model=UserReadModel)
def create_user(user: UserWriteModel):
    try:
        return User.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[UserReadModel])
def get_users():
    return User.get_users()

@router.post("/users/posts", response_model=UserPostReadModel)
def create_post(post: UserPostWriteModel):
    try:
        return UserPost.create_post(post)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}/posts", response_model=List[UserPostReadModel])
def get_posts_by_user(user_id: int):
    try:
        return UserPost.get_posts_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
