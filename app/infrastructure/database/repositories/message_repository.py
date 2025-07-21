from fastapi import Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.infrastructure.database.database_init import get_db_session
from app.domain.models.message import Message

class MessageRepository:
    db: AsyncSession
    
    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def create(self, message_data: Message) -> Message:
        new_message = Message(**message_data.dict())
        self.db.add(new_message)
        await self.db.commit()
        await self.db.refresh(new_message)
        return new_message

    async def get_all(self, session_id: str, skip: int = 0, limit: int = 20) -> List[Message]:
        query = select(Message).where(Message.session_id == session_id).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, message_id: str) -> Optional[Message]:
        query = select(Message).where(Message.id == message_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, message_id: str, message_data: Message) -> Optional[Message]:
        query = (
            update(Message)
            .where(Message.id == message_id)
            .values(**message_data.dict(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(message_id)

    async def delete(self, message_id: str) -> bool:
        query = delete(Message).where(Message.id == message_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
    
async def get_message_repository(db: AsyncSession = Depends(get_db_session)) -> MessageRepository:
        return MessageRepository(db)