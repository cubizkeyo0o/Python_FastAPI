from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.infrastructure.database.database_init import get_db_session
from app.domain.entities.auth import (
    Auth as DbAuth
)

class AuthRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db


    def save_token(self, user_id: int, access_token: str):
        new_auth = DbAuth(user_id=user_id, access_token=access_token)
        self.db.add(new_auth)
        self.db.commit()

async def get_auth_repository(db: AsyncSession = Depends(get_db_session)) -> AuthRepository:
        return AuthRepository(db)