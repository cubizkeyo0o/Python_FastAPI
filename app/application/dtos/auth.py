from datetime import datetime
from pydantic import BaseModel, UUID4

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class PayloadToken(BaseModel):
    subject: str
    expiration_time: str
    issued_at: datetime
    jwt_id: str

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime

    class Config:
        orm_mode = True