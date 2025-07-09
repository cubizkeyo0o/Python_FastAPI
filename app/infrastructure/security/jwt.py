import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Response
from datetime import timedelta, datetime, timezone

from app.application.dtos.auth import TokenPair, PayloadToken, PayloadTokenShort
from app.utils.exceptions.auth_exceptions import TokenExpiredException, InvalidTokenException
from app.config import ACCESS_TOKEN_EXPIRES_MINUTES, REFRESH_TOKEN_EXPIRES_MINUTES, ALGORITHM, SECRET_KEY, EXP

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