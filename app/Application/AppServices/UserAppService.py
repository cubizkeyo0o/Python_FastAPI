from typing import List, Optional

from fastapi import Depends
from Domain.Entities import User

from Infrastructure.Repositories import userrepository
from Dtos.UserDto import UserDto

class UserService:
    userRepository: userrepository

    def __init__(
        self, userRepository: userrepository = Depends()
        ) -> None:
        self.userRepository = userrepository

    def create(self, user_body: UserDto) -> User:
        return self.userRepository.create(
            User(name=user_body.name)
        )
    
    def update(
        self, user_id: int, user_body: UserDto
    ) -> User:
        return self.userRepository.update(
            user_body, User(name=user_body.name)
        )
   