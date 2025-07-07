from datetime import datetime
from pydantic import BaseModel, UUID4
from __future__ import annotations
from config import SUB, EXP, IAT, JTI

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class PayloadToken(BaseModel):
    subject: str
    expiration_time: str
    issued_at: datetime
    jwt_id: str

    @classmethod
    def from_short(cls, short: PayloadTokenShort) -> "PayloadToken":
        return cls(
            subject=short.SUB,
            expiration_time=short.EXP,
            issued_at=short.IAT,
            jwt_id=short.JTI
        )

class PayloadTokenShort(BaseModel):
    SUB: str
    EXP: str
    IAT: datetime
    JTI: str

    @classmethod
    def from_full(cls, full: PayloadToken) -> PayloadTokenShort:
        return cls(
            SUB=full.subject,
            EXP=full.expiration_time,
            IAT=full.issued_at,
            JTI=full.jwt_id
        )

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        orm_mode = True