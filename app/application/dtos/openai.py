from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class PromptRequest(BaseModel):
    session_id: UUID
    role: Optional[str] = None
    content: Optional[str] = None

class PromptResponse(BaseModel):
    response: str