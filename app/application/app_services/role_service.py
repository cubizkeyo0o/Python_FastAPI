from fastapi import Depends
from typing import List
from uuid import UUID

from app.domain.models.role import Role
from app.infrastructure.database.repositories.role_repository import RoleRepository, get_role_repository
from app.application.dtos.role import *

class RoleService:
    role_repo: RoleRepository

    def __init__(self,
                 role_repository: RoleRepository = Depends(get_role_repository)):
        self.role_repo = role_repository

    async def get_all_async(self) -> List[RoleResponse]:
        roles = await self.role_repo.get_all_async()
        return [RoleResponse.model_validate(role) for role in roles]

    async def create_async(self, role_data: RoleCreate) -> RoleResponse:
        role_created = await self.role_repo.create_async(Role(**role_data.model_dump()))
        return RoleResponse.model_validate(role_created)
    
    async def update_async(self, role_id: UUID, role_data: RoleUpdate) -> Optional[RoleResponse]:
        role_updated = await self.role_repo.update_async(role_id, role_data.model_dump())
        return RoleResponse.model_validate(role_updated) if role_updated else None

    async def delete_async(self, role_id: UUID) -> bool:
        return await self.role_repo.delete_async(role_id)