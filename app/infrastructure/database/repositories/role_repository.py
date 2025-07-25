from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, String
from typing import Optional, List
from uuid import uuid4, UUID, SafeUUID
from sqlalchemy.dialects import mysql

from app.infrastructure.database.database_init import get_db_session
from app.domain.models.role import Role
from app.domain.models.user_role import UserRole

class RoleRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db_session)) -> None:
        self.db = db
        
    async def get_by_id_async(self, id: UUID):
        query = select(Role).where(Role.id == str(id))
        queryResult = await self.db.execute(query)
        role = queryResult.scalars().first()
        return role
    
    async def get_by_names_async(self, role_names: list[str]):
        query = select(Role).where(Role.name.in_(role_names))
        result = await self.db.execute(query)
        roles = result.scalars().all()
        return roles
    
    async def get_by_name_async(self, role_name: str) -> Optional[Role]:
        query = select(Role).where(Role.normalized_name == role_name.strip().upper())
        result = await self.db.execute(query)
        return result.scalars().one_or_none()

    async def get_all_async(self) -> list[Role]:
        stmt = select(Role)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_async(self, role_create: Role) -> Role:
        role_create.id = uuid4()
        role_create.normalized_name = role_create.name.upper()
        self.db.add(role_create)
        return role_create
    
    async def update_async(self, role_id_update: UUID, values: dict) -> Optional[Role]:
        if not values:
            return await self.get_by_id_async(role_id_update)
        
        stmt = (
            update(Role)
            .where(Role.id == str(role_id_update))
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        
        await self.db.execute(stmt)
        await self.db.flush()
        
        result = await self.db.execute(select(Role).where(Role.id == role_id_update))
        user_db = result.scalar_one_or_none()
        return user_db if user_db else None
    
    async def delete_async(self, role_id_delete: UUID) -> bool:
        existing_role = await self.get_by_id_async(role_id_delete)

        if not existing_role:
            return False
        
        await self.db.delete(existing_role)
        return True

    async def get_roles_by_user(self, user_id: UUID) -> List[Role]:
        query = (
            select(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == str(user_id))
        )
        queryResult = await self.db.execute(query)
        roles = queryResult.scalars().all()
        return roles

async def get_role_repository(db: AsyncSession = Depends(get_db_session)) -> RoleRepository:
        return RoleRepository(db)