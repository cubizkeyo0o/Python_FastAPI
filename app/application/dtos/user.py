from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr, field_validator

class UserBase(BaseModel):
    user_name: str
    full_name: str

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: UUID4
    
    class Config:
        from_attributes = True

class UserRegister(UserBase):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    def verify_password_match(cls, v, values, **kwargs):
        password = values.get("password")

        if v != password:
            raise ValueError("The two passwords did not match.")

        return v


class UserLogin(BaseModel):
    user_name: str
    password: str