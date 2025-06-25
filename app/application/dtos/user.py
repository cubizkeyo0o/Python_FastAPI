from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr, field_validator

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID4
    
    class Config:
        from_attributes = True

class UserRegister(UserBase):
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def verify_password_match(cls, v, values, **kwargs):
        password = values.get("password")

        if v != password:
            raise ValueError("The two passwords did not match.")

        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CreateUserModel(BaseModel):
    name: str
    username: str
    email: Optional[str] = None

class UpdateUserModel(BaseModel):
    name: str
    username: str
    email: str

class ResponseUserModel(BaseModel):
    name: str
    email: str