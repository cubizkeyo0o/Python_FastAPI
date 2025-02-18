from typing import Optional
from pydantic import BaseModel

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