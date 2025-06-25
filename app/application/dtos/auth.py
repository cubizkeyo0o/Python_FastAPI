from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4

class TokenPair(BaseModel):
    access: str
    refresh: str

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        orm_mode = True

class RegisterUserModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUserModel(BaseModel):
    username: str
    password: str

class TokenResponseModel(BaseModel):
    access_token: str
    refresh_token: str