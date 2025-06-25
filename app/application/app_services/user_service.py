from fastapi import Depends
from typing import List

from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.application.models.user_model import(
    CreateUserModel,
    UpdateUserModel,
    ResponseUserModel
)
from app.domain.entities.user import (
    UserCreate,
    UserUpdate,
)

class UserService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends(get_user_repository)):
        self.userRepository = userRepository

    async def get_all_async(self) -> List[ResponseUserModel]:
        users = await self.userRepository.get_all_async()
        return [user.to_model() for user in users]

    async def create_async(self, user_body: CreateUserModel) -> ResponseUserModel:
        userCreate = await self.userRepository.create_async(
            UserCreate(name=user_body.name, username=user_body.username, email=user_body.email)
        )
        
        if not userCreate:
            raise Exception("User not found")
        
        return userCreate.to_model()

    async def update_async(self, user_id: int, user_body: UpdateUserModel) -> ResponseUserModel:
        userUpdate = await self.userRepository.update_async(
            id=user_id,
            user=UserUpdate(name=user_body.name, email=user_body.email)
        )

        if not userUpdate:
            raise Exception("User not found")
        
        return userUpdate.to_model()