from typing import List, Optional

from fastapi import Depends

from app.API.Models.UserModel import ResponseUserModel
from app.Domain.Entities.User import User
from app.Infrastructure.Repositories.UserRepository import UserRepository
from app.Application.Dtos.UserDto import UserDto

class UserService:
    userRepository: UserRepository

    def __init__(
        self, userRepository: UserRepository = Depends()
        ) -> None:
        self.userRepository = userRepository

    def create(self, user_body: UserDto) -> ResponseUserModel:
        return self.userRepository.create(
            user=User(name=user_body.name, email=user_body.email)
        )
    
    def update(
        self, user_id: int, user_body: UserDto
    ) -> ResponseUserModel:
        return self.userRepository.update(
            id=user_id,
            user=User(name=user_body.name, email=user_body.email)
        )
   