from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.Infrastructure.database.DatabaseInit import (
    get_db_connection,
)
from app.Domain.Entities.User import (
    User as DbUser,
    UserCreate, 
    UserUpdate
)

class UserRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_connection)) -> None:
        self.db = db

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

    async def create_async(self, user: UserCreate):
        async with get_db_connection() as db:
            user_create = DbUser(**user.model_dump())
            try:
                db.add(user_create)
                await db.commit()
                await db.refresh(user_create)
            except Exception as ex:
                raise Exception("abc") from ex

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
        query = select(DbUser).filter_by(id=id)
        queryResult = await self.db.execute(query)
        existing_user = queryResult.scalars().first()

        if not existing_user:
            return None
        
        await self.db.delete(existing_user)
        return {"message": "User deleted successfully"}

async def get_user_repository(db: AsyncSession = Depends(get_db_connection)) -> UserRepository:
        return UserRepository(db)