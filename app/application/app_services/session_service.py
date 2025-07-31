from uuid import UUID
from typing import Optional
from fastapi import Depends

from app.infrastructure.database.repositories.session_repository import SessionRepository, get_session_repository
from app.domain.models.session import Session
from app.application.dtos.session import *


class SessionService:
    repo: SessionRepository

    def __init__(self, repo: SessionRepository = Depends(get_session_repository)):
        self.repo = repo

    async def create_session(self, session_data: SessionCreate) -> SessionResponse:
        # first time create sesion, set default "New Chat"
        if not session_data.title or not session_data.title.strip():
            session_data.title = "New Chat"

        session = await self.repo.create(Session(**session_data.model_dump()))
        return SessionResponse.model_validate(session)

    async def get_session(self, session_id: UUID) -> Optional[SessionResponse]:
        session = await self.repo.get_by_id_async(session_id)
        return SessionResponse.model_validate(session) if session else None

    async def update_session(self, session_id: UUID, session_data: SessionUpdate) -> Optional[SessionResponse]:
        updated = await self.repo.update(session_id, session_data.model_dump())
        return SessionResponse.model_validate(updated) if updated else None

    async def delete_session(self, session_id: UUID) -> bool:
        return await self.repo.delete(session_id)
    
    async def generate_title_from_message(self, session_id: str, first_message: str) -> Optional[SessionResponse]:
        words = first_message.split()
        title = " ".join(words[:8]) + ("..." if len(words) > 8 else "")
        update_data = SessionUpdate(title=title)
        return await self.update_session(session_id, update_data)