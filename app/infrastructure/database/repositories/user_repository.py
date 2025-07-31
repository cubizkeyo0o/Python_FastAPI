from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import Optional, List
from uuid import uuid4, UUID

from app.infrastructure.database.database_session import get_db_session
from app.domain.models.user import UserDb

class UserRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def get_all_async(self):
        query = select(UserDb)
        queryExec = await self.db.execute(query)
        users = queryExec.scalars().all()

        if not users:
            return None
        return users

    async def get_by_email_async(self, email: str):
        query = select(UserDb).filter_by(email=email)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        return user
        
    async def get_by_id_async(self, id: UUID):
        query = select(UserDb).filter_by(id=str(id))
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        return user
    
    async def get_by_username_async(self, username: str):
        query = select(UserDb).filter_by(user_name=username)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        return user

    async def create_async(self, user_create: UserDb) -> UserDb:
        user_create.id = uuid4()
        self.db.add(user_create)
        return user_create
    
    async def update_async(self, user_id: UUID, values: dict) -> Optional[UserDb]:
        if not values:
            return await self.get_by_id_async(user_id)
        
        stmt = (
            update(UserDb)
            .where(UserDb.id == str(user_id))
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        
        await self.db.execute(stmt)
        await self.db.flush()
        
        result = await self.db.execute(select(UserDb).where(UserDb.id == user_id))
        user_db = result.scalar_one_or_none()
        return user_db if user_db else None
    
    async def delete_async(self, id: UUID) -> None:
        existing_user = self.get_by_id_async(id)

        if not existing_user:
            return None
        
        await self.db.delete(existing_user)
        return None

async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
        return UserRepository(db)