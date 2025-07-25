from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class MessageBase(BaseModel):
    user_id: UUID
    name: str

class MessageUpdate(BaseModel):
    content: str = None

class MessageCreate(BaseModel):
    session_id: Optional[UUID] = None
    role: Optional[str] = None
    message: Optional[str] = None

class MessageResponse(BaseModel):
    session_id: Optional[UUID] = None
    role: Optional[str] = None
    message: Optional[str] = None