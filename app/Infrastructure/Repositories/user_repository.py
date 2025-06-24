from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.infrastructure.database.database_init import get_db_session
from app.domain.entities.user import (
    User as DbUser,
    UserCreate, 
    UserUpdate
)

class UserRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def get_all_async(self):
        query = select(DbUser)
        queryExec = await self.db.execute(query)
        users = queryExec.scalars().all()

        if not users:
            return None
        return users

    async def get_by_email_async(self, email: str ):
        query = select(DbUser).filter_by(email=email)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        if not user:
            return None
        return user
        
    async def get_by_id_async(self, id: int):
        query = select(DbUser).filter_by(id=id)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        if not user:
            return None
        return user
    
    async def get_by_name(self, username: str):
        query = select(DbUser).filter_by(name=username)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        if not user:
            return None
        return user

    async def create_async(self, user: UserCreate):
            user_create = DbUser(**user.model_dump())
            self.db.add(user_create)
            await self.db.commit()
            await self.db.refresh(user_create)

            return user_create
    
    async def update_async(self, id: int, user: UserUpdate):
            query = select(DbUser).filter_by(id=id)
            queryResult = await self.db.execute(query)
            existing_user = queryResult.scalars().first()

            if not existing_user:
                return None
            
            for field, value in user.model_dump(exclude_unset=True).items:
                setattr(existing_user, field, value)
            
            await self.db.commit()
            return existing_user
    
    async def delete_async(self, id: int):
        async with get_db_session() as db:
            query = select(DbUser).filter_by(id=id)
            queryResult = await self.db.execute(query)
            existing_user = queryResult.scalars().first()

            if not existing_user:
                return None
            
            await self.db.delete(existing_user)
            return {"message": "User deleted successfully"}
    
    async def verify_password(self, username: str, password: str):
        async with get_db_session() as db:
            query = select(DbUser).filter_by(user_name=username, password_hash=password)
            queryResult = await db.execute(query)
            user_login = queryResult.scalars().first()
            if not user_login:
                return None
            return user_login

async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
        return UserRepository(db)