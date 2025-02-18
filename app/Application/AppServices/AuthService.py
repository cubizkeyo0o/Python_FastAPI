from datetime import timedelta
from app.Infrastructure.Repositories.AuthRepository import AuthRepository
from app.domain.entities.Auth import AuthHelper, RegisterUserDto, LoginUserDto, TokenResponseDto
from app.Infrastructure.Repositories.UserRepository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository
        self.auth_repository = AuthRepository

    def register_user(self, user_data: RegisterUserDto):
        existing_user = self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise ValueError("Username already exists")

        hashed_password = AuthHelper.hash_password(user_data.password)

        new_user = self.user_repository.create(user_data.username, user_data.email, hashed_password)

        return {"message": "User registered successfully", "user_id": new_user.id}

    def login_user(self, login_data: LoginUserDto):
        user = self.user_repository.get_by_username(login_data.username)
        if not user or not AuthHelper.verify_password(login_data.password, user.passwordhash):
            raise ValueError("Invalid credentials")

        access_token = AuthHelper.create_access_token({"sub": user.username}, timedelta(minutes=60))

        self.auth_repository.save_token(user.id, access_token)

        return TokenResponseDto(access_token=access_token, refresh_token=None)
