from fastapi import Depends
from uuid import UUID
from typing import List, Optional
from app.infrastructure.database.repositories.message_repository import MessageRepository, get_message_repository
from app.application.dtos.message import MessageCreate, MessageUpdate, MessageResponse
from app.domain.models.message import Message
from app.application.app_services.session_service import SessionService

class MessageService:
    repo: MessageRepository
    session_service: SessionService

    def __init__(self, repo: MessageRepository = Depends(get_message_repository), session_service: SessionService = Depends()):
        self.repo = repo
        self.session_service = session_service

    async def create_message(self, message_data: MessageCreate) -> MessageResponse:
        # lower role to match with content gemini ai
        message_data.role = message_data.role.lower()
        message = await self.repo.create(Message(**message_data.model_dump()))
        return MessageResponse.model_validate(message)

    async def get_messages(self, session_id: UUID, skip: int = 0, limit: int = 20) -> List[MessageResponse]:
        messages = await self.repo.get_all(session_id=session_id, skip=skip, limit=limit)
        return [MessageResponse.model_validate(m) for m in messages]

    async def get_message(self, message_id: UUID) -> Optional[MessageResponse]:
        message = await self.repo.get_by_id_async(message_id)
        return MessageResponse.model_validate(message) if message else None

    async def update_message(self, message_id: UUID, message_data: MessageUpdate) -> Optional[MessageResponse]:
        updated = await self.repo.update(message_id, message_data.model_dump())
        return MessageResponse.model_validate(updated) if updated else None

    async def delete_message(self, message_id: UUID) -> bool:
        return await self.repo.delete(message_id)