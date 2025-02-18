import jwt

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.domain.Base import EntityMeta
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthHelper:
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=AuthHelper.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthHelper.SECRET_KEY, algorithm=AuthHelper.ALGORITHM)

class Auth(EntityMeta):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    access_token: Mapped[str] = mapped_column(String(500), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
    user = relationship("User", back_populates="auth_sessions")

class RegisterUserDto(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUserDto(BaseModel):
    username: str
    password: str

class TokenResponseDto(BaseModel):
    access_token: str
    refresh_token: str