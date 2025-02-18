from fastapi import Depends

from app.Infrastructure.Repositories.UserRepository import UserRepository, get_user_repository
from app.Application.Models.UserModel import(
    CreateUserModel,
    UpdateUserModel,
    ResponseUserModel
)
from app.Domain.Entities.User import (
    UserCreate,
    UserUpdate,
)

class UserService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends(get_user_repository)):
        self.userRepository = userRepository

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