from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

from app.application.dtos.user import UserResponse

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class TokenPairRegisterResponse(TokenPair):
    user: UserResponse

class PayloadToken(BaseModel):
    sub: str
    exp: Optional[str] = None
    iat: datetime
    jti: Optional[str] = None

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        from_attributes = True