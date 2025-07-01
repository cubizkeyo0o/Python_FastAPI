import jwt
from datetime import timedelta, datetime, timezone

from app. application.dtos.auth import TokenPair, PayloadToken
from app.config import ACCESS_TOKEN_EXPIRES_MINUTES, REFRESH_TOKEN_EXPIRES_MINUTES, ALGORITHM, SECRET_KEY

REFRESH_COOKIE_NAME = "refresh"
SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"

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
        access_token=_create_access_token(payload={**payload.model_dump()}),
        refresh_token=_create_refresh_token(payload={**payload.model_dump()}),
    )