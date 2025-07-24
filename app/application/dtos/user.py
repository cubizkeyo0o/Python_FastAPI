from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID

from app.utils.exceptions.common_exceptions import NotMatchException

class UserBase(BaseModel):
    user_name: str
    full_name: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_name: Optional[str] = None
    roles: Optional[List[str]] = None
    password: Optional[str] = None

    @field_validator("roles", mode="before")
    def normalize_roles(cls, v):
        if isinstance(v, list) and all(isinstance(item, str) for item in v):
            return [role.strip().upper() for role in v]

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    user_name: str
    roles: Optional[List[str]] = None
    email: EmailStr

    class Config:
        from_attributes = True


class User(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True

class UserRegister(UserBase):
    email: Optional[EmailStr] = None
    password: str
    confirm_password: str
    roles: List[str]

    @field_validator("confirm_password")
    def verify_password_match(cls, v, values):
        password = values.data.get("password")

        if v != password:
            raise NotMatchException("The two passwords did not match.")

        return v
    
    @field_validator("roles", mode="before")
    def normalize_roles(cls, v):
        if isinstance(v, list) and all(isinstance(item, str) for item in v):
            return [role.strip().upper() for role in v]
        raise ValueError("roles must be a list of strings")


class UserLogin(BaseModel):
    user_name: str
    password: str