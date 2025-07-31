from fastapi import Depends
from uuid import UUID, uuid4
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func

from app.infrastructure.database.database_session import get_db_session
from app.domain.models.message import Message

class MessageRepository:
    db: AsyncSession
    
    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def create(self, new_message: Message) -> Message:
        new_message.id = uuid4()
        self.db.add(new_message)
        await self.db.flush()
        await self.db.refresh(new_message)
        return new_message

    async def get_all(self, session_id: UUID, skip: int = 0, limit: int = 20) -> List[Message]:
        query = select(Message).where(Message.session_id == str(session_id)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id_async(self, message_id: UUID) -> Optional[Message]:
        query = select(Message).where(Message.id == str(message_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def count_messages_by_session(self, session_id: str) -> int:
        stmt = select(func.count(Message.id)).where(Message.session_id == str(session_id))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def update(self, message_id: UUID, values: dict) -> Optional[Message]:
        if not values:
            return await self.get_by_id_async(message_id)
        
        stmt = (
            update(Message)
            .where(Message.id == str(message_id))
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        
        await self.db.execute(stmt)
        await self.db.flush()
        
        result = await self.db.execute(select(Message).where(Message.id == message_id))
        message_updated = result.scalar_one_or_none()
        return message_updated if message_updated else None
    
    async def delete(self, message_id: UUID) -> bool:
        query = delete(Message).where(Message.id == str(message_id))
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
    
async def get_message_repository(db: AsyncSession = Depends(get_db_session)) -> MessageRepository:
        return MessageRepository(db)