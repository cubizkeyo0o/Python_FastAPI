from pydantic import BaseModel, EmailStr

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