from typing import List, Optional
from pydantic import BaseModel

class CreateUserModel(BaseModel):
    name: str
    email: Optional[str] = None

class UpdateUserModel(CreateUserModel):
    id: int

class ResponseUserModel(BaseModel):
    id: int
    name: str