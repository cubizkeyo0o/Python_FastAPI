from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        orm_mode = True