from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.Infrastructure.database.DatabaseInit import get_db_session
from app.domain.entities.Auth import (
    RegisterUserDto,
    LoginUserDto,
    TokenResponseDto,
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