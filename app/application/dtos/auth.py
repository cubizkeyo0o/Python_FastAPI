from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

from app.application.dtos.user import UserResponse

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class TokenPairRegisterResponse(TokenPair):
    user: UserResponse

class PayloadToken(BaseModel):
    subject: str
    expiration_time: Optional[str] = None
    issued_at: datetime
    jwt_id: str
    
    def to_short(self) -> PayloadTokenShort:
        return PayloadTokenShort(
            sub=self.subject,
            exp=self.expiration_time,
            iat=self.issued_at,
            jti=self.jwt_id
        )

class PayloadTokenShort(BaseModel):
    sub: str
    exp: Optional[str] = None
    iat: datetime
    jti: str

    def to_full(self) -> PayloadToken:
        return PayloadToken(
            subject=self.sub,
            expiration_time=self.exp,
            issued_at=self.iat,
            jwt_id=self.jti
        )

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        from_attributes = True