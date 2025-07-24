from fastapi import Depends
from typing import List
from uuid import UUID

from app.utils.exceptions.auth_exceptions import InvalidCredentialsException
from app.utils.exceptions.common_exceptions import EntityNotFoundException, RequiredException, InternalServerErrorException
from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.infrastructure.database.repositories.role_repository import RoleRepository, get_role_repository
from app.infrastructure.database.repositories.user_role_repository import UserRoleRepository, get_user_role_repository
from app.infrastructure.security.hash import hash_password, verify_password
from app.domain.models.user import UserDb
from app.application.dtos.user import(
    UserLogin,
    UserRegister,
    UserUpdate,
    UserResponse
)

class UserService:
    user_repo: UserRepository
    role_repo: RoleRepository
    user_role_repo: UserRoleRepository

    def __init__(self,
                 user_repository: UserRepository = Depends(get_user_repository),
                 role_repository: RoleRepository = Depends(get_role_repository),
                 user_role_repository: UserRoleRepository = Depends(get_user_role_repository)):
        self.user_repo = user_repository
        self.role_repo = role_repository
        self.user_role_repo = user_role_repository

    async def login_account(self, user_login: UserLogin) -> UserResponse:
        user_exist = await self.user_repo.get_by_username_async(username=user_login.user_name)

        if user_exist is None:
            raise InvalidCredentialsException("Invalid username")
        
        is_valid_password = verify_password(user_login.password, user_exist.password_hash)

        if not is_valid_password:
            raise InvalidCredentialsException("Invalid password")
        
        return UserResponse(id=user_exist.id, full_name=user_exist.full_name, user_name=user_exist.user_name, email=user_exist.email)

    async def get_all_async(self) -> List[UserResponse]:
        users = await self.user_repo.get_all_async()
        if not users:
            return []
        return [UserResponse(id=user.id, full_name=user.full_name, user_name=user.user_name, email=user.email) for user in users]
    
    async def check_exist_email(self, email: str) -> bool:
        user = await self.user_repo.get_by_email_async(email=email)
        if not user:
            return False
        return True

    async def check_exist_user_name(self, name: str) -> bool:
        user = await self.user_repo.get_by_username_async(username=name)
        if not user:
            return False
        return True

    async def create_async(self, user_register: UserRegister) -> UserResponse:
        new_user = UserDb(full_name=user_register.full_name, user_name=user_register.user_name, email=user_register.email)
        
        # hash password
        new_user.password_hash = hash_password(user_register.password)

        # get exist roles
        user_role_ids = await self.check_and_get_valid_role(user_register.roles)

        if not user_register.roles:
            raise RequiredException("Roles is required")

        if not user_role_ids:
            raise EntityNotFoundException("Roles not found")

        # create user
        user_created = await self.user_repo.create_async(new_user)
        
        # add role user
        add_role_user_success = await self.user_role_repo.add_user_roles(user_role_ids, user_created.id)
        
        if not add_role_user_success:
            raise InternalServerErrorException("Add roles for user failed")

        return UserResponse(id=user_created.id, email=user_created.email, full_name=user_created.full_name, user_name=user_created.user_name)

    async def get_by_id_async(self, user_id: UUID) -> UserResponse:
        user_exist = await self.user_repo.get_by_id_async(id=user_id)
        
        if user_exist is None:
            raise EntityNotFoundException("User not found")
        
        return UserResponse(id=user_exist.id, full_name=user_exist.full_name, user_name=user_exist.user_name, email=user_exist.email)

    async def update_async(self, user_id: UUID, user_body: UserUpdate) -> UserResponse:
        user_exist = await self.user_repo.get_by_id_async(user_id)
        
        if user_exist is None:
            raise EntityNotFoundException("User not found")

        if user_body.password is not None:
            is_change_password = not verify_password(user_body.password, user_exist.password_hash)
            
        if is_change_password is not None and is_change_password:
            user_exist.password_hash = hash_password(user_body.password)

        user_exist.full_name = user_body.full_name
        user_exist.user_name = user_body.user_name
        user_exist.email = user_body.email
        
        user_updated = await self.user_repo.update_async(user_id, user_exist)
        
        roles_updated = False
        if user_body.roles:
            role_ids = await self.check_and_get_valid_role(user_body.roles)
            roles_updated = await self.user_role_repo.update_user_roles(role_ids, user_id)

        if not roles_updated:
            raise InternalServerErrorException("Update roles for user failed")

        return UserResponse(id=user_updated.id, email=user_updated.email, full_name=user_updated.full_name, user_name=user_updated.user_name)
    
    async def delete_async(self, user_id: UUID) -> None:
        user_delete = await self.user_repo.get_by_id_async(id=user_id)

        if not user_delete:
            raise EntityNotFoundException("User not found")

        await self.user_repo.delete_async(user_id)
        await self.user_role_repo.delete_by_user_id_async(user_id)
        
        return None
    
    async def check_and_get_valid_role(self, name_roles: List[str]) -> List[UUID] | None:
        exist_roles = await self.role_repo.get_all_async()
        allowed_normalized_roles =  [role.normalized_name for role in exist_roles]
        name_roles = [role.upper() for role in name_roles]

        if all(role not in allowed_normalized_roles for role in name_roles):
            return None
        
        return [
            role.id for role in exist_roles
            if role.normalized_name in name_roles
        ]
