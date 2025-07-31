from fastapi import Depends
from typing import List
from uuid import UUID

from app.domain.models.role import Role
from app.utils.exceptions.common_exceptions import DuplicatedException, EntityNotFoundException, ConflictException
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
        exist_role = await self.role_repo.get_by_name_async(role_data.name)

        if exist_role:
            raise DuplicatedException("Role already exist")

        role_created = await self.role_repo.create_async(Role(**role_data.model_dump()))
        return RoleResponse.model_validate(role_created)
    
    async def update_async(self, role_id: UUID, role_data: RoleUpdate) -> Optional[RoleResponse]:
        exist_role = await self.role_repo.get_by_id_async(role_id)
        
        if not exist_role:
            raise EntityNotFoundException("Role not found")

        if exist_role and exist_role.concurrency_stamp != role_data.concurrency_stamp:
            raise ConflictException("Concurrency conflict. The data has been modified by another process.")

        role_updated = await self.role_repo.update_async(role_id, role_data.model_dump())
        return RoleResponse.model_validate(role_updated) if role_updated else None

    async def delete_async(self, role_id: UUID) -> bool:
        is_exist_role = await self.role_repo.get_by_id_async(role_id)

        if not is_exist_role:
            raise EntityNotFoundException("Role not found")

        return await self.role_repo.delete_async(role_id)