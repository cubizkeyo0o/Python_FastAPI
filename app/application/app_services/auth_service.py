from datetime import timedelta
from fastapi import Depends
from app.infrastructure.database.repositories.auth_repository import AuthRepository
from app.domain.entities.auth import AuthHelper, RegisterUserDto, TokenResponseDto
from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.domain.entities.user import UserCreate

class AuthService:
    user_Repository = UserRepository
    
    def __init__(self, userRepository: UserRepository = Depends(get_user_repository)):
        self.user_repository = userRepository
        self.auth_repository = AuthRepository

    def register_user(self, user_data: RegisterUserDto):
        existing_user = self.user_repository.get_by_name(user_data.username)
        if not existing_user:
            raise ValueError("Username already exists")

        hashed_password = AuthHelper.hash_password(user_data.password)

        new_user = self.user_repository.create_async(UserCreate(name=user_data.name, email=user_data.email, username=user_data.username, password_hash=hashed_password))

        return {"message": "User registered successfully", "user_id": new_user.id}

    def login_user(self, user_name: str, password: str):
        user = self.user_repository.get_by_name(user_name)
        if not user or not AuthHelper.verify_password(password, user.passwordhash):
            raise ValueError("Invalid credentials")

        access_token = AuthHelper.create_access_token({"sub": user.username}, timedelta(minutes=60))

        self.auth_repository.save_token(user.id, access_token)

        return TokenResponseDto(access_token=access_token, refresh_token=None)
