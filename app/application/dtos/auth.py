from __future__ import annotations
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
    expiration_time: str
    issued_at: datetime
    jwt_id: str
    
    @classmethod
    def to_short(cls) -> PayloadTokenShort:
        return PayloadTokenShort(
            sub=cls.subject,
            exp=cls.expiration_time,
            iat=cls.issued_at,
            jti=cls.jwt_id
        )

class PayloadTokenShort(BaseModel):
    sub: str
    exp: str
    iat: datetime
    jti: str

    @classmethod
    def to_full(cls) -> PayloadToken:
        return PayloadToken(
            subject=cls.sub,
            expiration_time=cls.exp,
            issued_at=cls.iat,
            jwt_id=cls.jti
        )

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        from_attributes = True