from uuid import UUID
from typing import Optional
from fastapi import Depends

from app.infrastructure.database.repositories.session_repository import SessionRepository, get_session_repository
from app.infrastructure.database.repositories.message_repository import MessageRepository, get_message_repository
from app.domain.models.session import Session
from app.application.dtos.session import *


class SessionService:
    repo: SessionRepository
    message_repo: MessageRepository

    def __init__(self,
                 repo: SessionRepository = Depends(get_session_repository),
                 message_repo: MessageRepository = Depends(get_message_repository)):
        self.repo = repo
        self.message_repo = message_repo

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
    
    async def count_messages_by_session(self, session_id: UUID) -> int:
        return await self.message_repo.count_messages_by_session(session_id)