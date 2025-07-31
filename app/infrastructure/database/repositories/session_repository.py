from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import Depends
from uuid import UUID, uuid4
from sqlalchemy.dialects import mysql

from app.infrastructure.database.database_session import get_db_session
from app.domain.models.session import Session


class SessionRepository:
    db: AsyncSession
    
    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def create(self, new_session: Session) -> Session:
        new_session.id = uuid4()
        self.db.add(new_session)
        await self.db.flush()
        await self.db.refresh(new_session)
        return new_session

    async def get_by_id_async(self, session_id: UUID) -> Optional[Session]:
        query = select(Session).where(Session.id == str(session_id))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update(self, session_id: UUID, values: dict) -> Optional[Session]:
        if not values:
            return await self.get_by_id_async(session_id)
        
        stmt = (
            update(Session)
            .where(Session.id == str(session_id))
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        
        await self.db.execute(stmt)
        await self.db.flush()
        
        result = await self.db.execute(select(Session).where(Session.id == session_id))
        role_updated = result.scalar_one_or_none()
        return role_updated if role_updated else None

    async def delete(self, session_id: UUID) -> bool:
        query = delete(Session).where(Session.id == str(session_id))
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
    
async def get_session_repository(db: AsyncSession = Depends(get_db_session)) -> SessionRepository:
        return SessionRepository(db)