from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class SessionBase(BaseModel):
    user_id: UUID
    title: str

class SessionUpdate(BaseModel):
    summary_context: Optional[str] = None
    extra_metadata: Optional[str] = None

class SessionCreate(BaseModel):
    user_id: Optional[UUID] = None
    title: Optional[str] = None
    summary_context: Optional[str] = None
    extra_metadata: Optional[str] = None

class SessionResponse(BaseModel):
    title: Optional[str] = None
    summary_context: Optional[str] = None
    extra_metadata: Optional[str] = None

    class Config:
        from_attributes = True