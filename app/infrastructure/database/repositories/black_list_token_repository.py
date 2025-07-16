from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.infrastructure.database.database_init import get_db_session
from app.domain.models.black_list_token import BlackListToken as BlackListTokenDB

class BlackListTokenRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def get_by_id_async(self, id: UUID) -> BlackListTokenDB | None:
        query = select(BlackListTokenDB).filter_by(id=id)
        queryResult = await self.db.execute(query)
        user = queryResult.scalars().first()
        return user
    
async def get_black_list_token_repository(db: AsyncSession = Depends(get_db_session)) -> BlackListTokenRepository:
        return BlackListTokenRepository(db)
    