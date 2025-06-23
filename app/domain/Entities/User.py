from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel

from app.Application.Models.UserModel import ResponseUserModel

from app.domain.Base import EntityMeta

class User(EntityMeta):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    user_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'User({self.id}, "{self.name}")'

    def to_model(self) -> ResponseUserModel:
        return ResponseUserModel(name=self.name, email=self.email)
    
class UserCreate(BaseModel):
    name: str
    username : str
    email: str
    password_hash: str

class UserInDB(UserCreate):
    id: int

class UserUpdate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    username: str
    email: str
    name: str