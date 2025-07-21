import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Response, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from uuid import UUID

from app.application.dtos.auth import TokenPair, PayloadToken, PayloadTokenShort
from app.utils.exceptions.auth_exceptions import TokenExpiredException, InvalidTokenException, MissingTokenException, BlackListTokenException
from app.utils.exceptions.common_exceptions import EntityNotFoundException, NoRoleAssignedException
from app.infrastructure.database.repositories.user_repository import UserRepository, get_user_repository
from app.infrastructure.database.repositories.black_list_token_repository import BlackListTokenRepository, get_black_list_token_repository
from app.config import ACCESS_TOKEN_EXPIRES_MINUTES, REFRESH_TOKEN_EXPIRES_MINUTES, ALGORITHM, SECRET_KEY, EXP

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

async def authentication_request_handle(request: Request,
                                        token: str = Depends(oauth2_scheme),
                                        user_repo: UserRepository = Depends(get_user_repository),
                                        black_list_token_repo: BlackListTokenRepository = Depends(get_black_list_token_repository)):
    if not token:
        raise MissingTokenException()

    try:
        payload = decode_access_token(token)
    except Exception:
        raise InvalidTokenException()
    
    black_list_token = await black_list_token_repo.get_by_id_async(id=UUID(payload.jwt_id))
    if black_list_token:
        raise BlackListTokenException()

    user_id = payload.subject
    if not user_id:
        raise InvalidTokenException()

    user = await user_repo.get_by_id_async(UUID(user_id))
    if not user:
        raise EntityNotFoundException(message="User not found")
    
    roles = payload.roles
    if not roles:
        raise NoRoleAssignedException(message="User does not have any assigned roles.")
    
    request.state.user = user
    request.state.roles = roles
    
def _create_access_token(payload: dict, expires_delta: timedelta = None):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRES_MINUTES
    )

    payload[EXP] = expire

    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

def _create_refresh_token(payload: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)

    payload[EXP] = expire

    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)


def create_token_pair(payload: PayloadToken) -> TokenPair:
    return TokenPair(
        access_token=_create_access_token(payload={**payload.to_short().model_dump()}),
        refresh_token=_create_refresh_token(payload={**payload.to_short().model_dump()}),
    )

def decode_access_token(token: str) -> PayloadToken:
    try:
        payload_decoded = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        short_payload = PayloadTokenShort(**payload_decoded)
        return short_payload.to_full()
    
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except InvalidTokenError as e:
        raise InvalidTokenException(f"Invalid token: {str(e)}")
    
def refresh_token_state(token: str):
    try:
        payload_decoded = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError as ex:
        raise InvalidTokenException(f"Invalid token: {str(ex)}")

    return _create_access_token(payload={**payload_decoded})

def add_refresh_token_cookie(response: Response, token: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
    exp.replace(tzinfo=timezone.utc)

    response.set_cookie(
        key="refresh",
        value=token,
        expires=int(exp.timestamp()),
        httponly=True,
    )