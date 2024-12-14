from typing import List
from Models.models import UserReadModel, UserWriteModel, UserPostReadModel, UserPostWriteModel
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///osucs461.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    posts = relationship("UserPostDB", back_populates="user")

class UserPostDB(Base):
    __tablename__ = "user_post"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("UserDB", back_populates="posts")

Base.metadata.create_all(bind=engine)

class User:
    @staticmethod
    def create_user(user_data: UserWriteModel) -> UserReadModel:
        session = SessionLocal()
        try:
            new_user = UserDB(username=user_data.username, email=user_data.email)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return UserReadModel.from_orm(new_user)
        finally:
            session.close()

    @staticmethod
    def get_users() -> List[UserReadModel]:
        session = SessionLocal()
        try:
            users = session.query(UserDB).all()
            return [UserReadModel.from_orm(user) for user in users]
        finally:
            session.close()

class UserPost:
    @staticmethod
    def create_post(post_data: UserPostWriteModel) -> UserPostReadModel:
        session = SessionLocal()
        try:
            user = session.query(UserDB).filter(UserDB.id == post_data.user_id).first()
            if not user:
                raise ValueError("User does not exist")

            new_post = UserPostDB(user_id=post_data.user_id, content=post_data.content)
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
            return UserPostReadModel.from_orm(new_post)
        finally:
            session.close()

    @staticmethod
    def get_posts_by_user(user_id: int) -> List[UserPostReadModel]:
        session = SessionLocal()
        try:
            posts = session.query(UserPostDB).filter(UserPostDB.user_id == user_id).all()
            return [UserPostReadModel.from_orm(post) for post in posts]
        finally:
            session.close()
