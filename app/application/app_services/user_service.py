from fastapi import Depends
from typing import List
from uuid import UUID

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

    async def get_all_async(self) -> List[UserResponse]:
        users = await self.userRepository.get_all_async()
        return [user.to_model() for user in users]
    
    async def check_exist_email(self, email: str) -> bool:
        user = await self.userRepository.get_by_email_async(email=email)
        if not user:
            return False
        return True

    async def check_exist_user_name(self, name: str) -> bool:
        user = await self.userRepository.get_by_username_async(name=name)
        if not user:
            return False
        return True

    async def create_async(self, user_register: UserRegister) -> UserResponse:
        new_user = user_register.model_dump(exclude={"confirm_password"})
        
        # hash password
        new_user["password_hash"] = hash_password(user_register.password)
        
        user_Created = await self.userRepository.create_async(new_user)
        
        return user_Created

    async def update_async(self, user_id: int, user_body: UpdateUserModel) -> UserResponse:
        userUpdate = await self.userRepository.update_async(
            id=user_id,
            user=UserUpdate(name=user_body.name, email=user_body.email)
        )

        if not userUpdate:
            raise Exception("User not found")
        
        return userUpdate.to_model()