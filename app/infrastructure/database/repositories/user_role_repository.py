from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, String
from typing import Optional, List
from uuid import uuid4, UUID

from app.infrastructure.database.database_init import get_db_session
from app.domain.models.role import Role
from app.domain.models.user_role import UserRole

class UserRoleRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db

    async def add_user_roles(self, role_ids: List[UUID], user_id: UUID) -> bool:
        user_roles = [UserRole(user_id=user_id, role_id=role_id) for role_id in role_ids]
        self.db.add_all(user_roles)

        return True
    
    async def update_user_roles(self, role_ids: List[UUID], user_id: UUID) -> bool:
        self.delete_by_user_id_async(user_id=user_id)
        self.add_user_roles(role_ids=role_ids, user_id=user_id)
        
        return True
    
    async def delete_by_user_id_async(self, user_id: UUID) -> bool:
        stmt = select(UserRole).where(user_id==str(user_id))
        exist_record = await self.db.execute(stmt)

        for user_role in exist_record:
            await self.db.delete(user_role)

        return True

async def get_user_role_repository(db: AsyncSession = Depends(get_db_session)) -> UserRoleRepository:
        return UserRoleRepository(db)