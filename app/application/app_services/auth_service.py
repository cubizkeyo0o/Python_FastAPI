from datetime import datetime, timezone
from fastapi import Depends
from uuid import uuid4, UUID

from app.application.dtos.auth import TokenPair, PayloadToken
from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.infrastructure.security.jwt import create_token_pair
class AuthService:
    user_Repository = UserRepository
    
    def __init__(self, userRepository: UserRepository = Depends(get_user_repository)):
        self.user_repository = userRepository

    def generate_token_pair(self, user_id: UUID) -> TokenPair:
        payload = PayloadToken(sub=str(user_id), jti=str(uuid4()), iat=datetime.now(timezone.utc))
        return create_token_pair(payload=payload)

        
