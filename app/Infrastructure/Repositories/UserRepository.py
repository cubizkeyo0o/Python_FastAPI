from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.Infrastructure.database.DatabaseInit import get_db_session
from app.domain.entities.User import (
    User as DbUser,
    UserCreate, 
    UserUpdate
)

class UserRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def get_all_async(self):
        try:
            query = select(DbUser)
            queryExec = await self.db.execute(query)
            users = queryExec.scalars().all()

            if not users:
                return None
            return users
        except Exception as ex: 
            check = ex

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
        async with get_db_session() as db:
            user_create = DbUser(**user.model_dump())
            try:
                db.add(user_create)
                await db.commit()
                await db.refresh(user_create)
            except Exception as ex:
                raise Exception("abc") from ex

            return user_create
    
    async def update_async(self, id: int, user: UserUpdate):
        async with get_db_session() as db:
            query = select(DbUser).filter_by(id=id)
            queryResult = await db.execute(query)
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