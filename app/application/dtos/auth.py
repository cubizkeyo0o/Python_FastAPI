from datetime import datetime
from pydantic import BaseModel, UUID4
from __future__ import annotations

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
            SUB=cls.subject,
            EXP=cls.expiration_time,
            IAT=cls.issued_at,
            JTI=cls.jwt_id
        )

class PayloadTokenShort(BaseModel):
    SUB: str
    EXP: str
    IAT: datetime
    JTI: str

    @classmethod
    def to_full(cls) -> PayloadToken:
        return PayloadToken(
            subject=cls.SUB,
            expiration_time=cls.EXP,
            issued_at=cls.IAT,
            jwt_id=cls.JTI
        )

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        from_attributes = True