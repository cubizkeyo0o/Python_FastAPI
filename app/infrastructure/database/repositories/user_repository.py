from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from app.infrastructure.database.database_init import get_db_session
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
        
    async def get_by_id_async(self, id: int):
        query = select(UserDb).filter_by(id=id)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        return user
    
    async def get_by_username_async(self, username: str):
        query = select(UserDb).filter_by(username=username)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        return user

    async def create_async(self, user_create: UserDb) -> UserDb:
        user_create.id = uuid4()
        self.db.add(user_create)
        await self.db.commit()

        return user_create
    
    async def update_async(self, user_update: UserDb):
        await self.db.refresh(user_update)
        await self.db.commit()
        return user_update
    
    async def delete_async(self, id: int):
        query = select(UserDb).filter_by(id=id)
        queryResult = await self.db.execute(query)
        existing_user = queryResult.scalars().first()

        if not existing_user:
            return None
        
        await self.db.delete(existing_user)
        return {"message": "User deleted successfully"}

async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
        return UserRepository(db)