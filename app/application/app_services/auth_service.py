from datetime import datetime, timezone
from fastapi import Depends
from uuid import uuid4, UUID

from app.application.dtos.auth import TokenPair, PayloadToken
from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.infrastructure.database.repositories.black_list_token_repository import BlackListTokenRepository, get_black_list_token_repository

from app.infrastructure.security.jwt import create_token_pair, decode_access_token
class AuthService:
    user_repo = UserRepository
    black_list_token_repo = BlackListTokenRepository
    
    def __init__(self,
                 user_repository: UserRepository = Depends(get_user_repository),
                 black_list_token_repository: BlackListTokenRepository = Depends(get_black_list_token_repository)):
        self.user_repo = user_repository
        self.black_list_token_repo = black_list_token_repository

    def generate_token_pair(self, user_id: UUID) -> TokenPair:
        payload = PayloadToken(sub=str(user_id), jti=str(uuid4()), iat=datetime.now(timezone.utc))
        return create_token_pair(payload=payload)

    async def check_access_token(self, token_check: str) -> PayloadToken:
        payload = decode_access_token(token=token_check)

        black_list_token = await self.black_list_token_repo.get_by_id_async(id=payload.jwt_id)
        if black_list_token:
            raise Exception("Token is blacklisted")

        return payload
