from fastapi import Depends
from typing import List
from uuid import UUID

from app.utils.exceptions.auth_exceptions import InvalidCredentialsException
from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.infrastructure.security.hash import hash_password, verify_password
from app.domain.models.user import UserDb
from app.application.dtos.user import(
    UserLogin,
    UserRegister,
    UserUpdate,
    UserResponse
)

class UserService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends(get_user_repository)):
        self.userRepository = userRepository

    async def login_account(self, user_login: UserLogin) -> UserResponse:
        user_exist = await self.userRepository.get_by_username_async(username=user_login.user_name)

        if user_exist is None:
            raise InvalidCredentialsException("Invalid username")
        
        is_valid_password = verify_password(user_login.password, user_exist.password_hash)

        if not is_valid_password:
            raise InvalidCredentialsException("Invalid password")
        
        return UserResponse(id=user_exist.id, full_name=user_exist.full_name, user_name=user_exist.user_name, email=user_exist.email)

    async def get_all_async(self) -> List[UserResponse]:
        users = await self.userRepository.get_all_async()
        return [UserResponse(id=user.id, full_name=user.full_name, user_name=user.user_name, email=user.email) for user in users]
    
    async def check_exist_email(self, email: str) -> bool:
        user = await self.userRepository.get_by_email_async(email=email)
        if not user:
            return False
        return True

    async def check_exist_user_name(self, name: str) -> bool:
        user = await self.userRepository.get_by_username_async(username=name)
        if not user:
            return False
        return True

    async def create_async(self, user_register: UserRegister) -> UserResponse:
        new_user = UserDb(full_name=user_register.full_name, user_name=user_register.user_name, email=user_register.email)
        
        # hash password
        new_user.password_hash = hash_password(user_register.password)

        user_created = await self.userRepository.create_async(new_user)
        
        return UserResponse(id=user_created.id, email=user_created.email, full_name=user_created.full_name, user_name=user_created.user_name)

    async def get_by_id_async(self, user_id: UUID) -> UserResponse:
        user_exist = await self.userRepository.get_by_id_async(id=user_id)
        
        if user_exist is None:
            raise Exception("User not found")
        
        return UserResponse(id=user_exist.id, full_name=user_exist.full_name, user_name=user_exist.user_name, email=user_exist.email)

    async def update_async(self, user_id: UUID, user_body: UserUpdate) -> UserResponse:
        user_exist = await self.userRepository.get_by_id_async(user_id)
        
        if user_exist is None:
            raise Exception("User not found")

        if user_body.password is not None:
            is_change_password = not verify_password(user_body.password, user_exist.password_hash)
            
        if is_change_password is not None and is_change_password:
            user_exist.password_hash = hash_password(user_body.password)
        
        user_exist.full_name = user_body.full_name
        user_exist.user_name = user_body.user_name
        user_exist.email = user_body.email
        
        user_updated = await self.userRepository.update_async(user_exist)

        return UserResponse(id=user_updated.id, email=user_updated.email, full_name=user_updated.full_name, user_name=user_updated.user_name)
