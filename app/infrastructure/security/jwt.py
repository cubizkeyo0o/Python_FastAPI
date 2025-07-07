import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import timedelta, datetime, timezone

from app. application.dtos.auth import TokenPair, PayloadToken, PayloadTokenShort
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
        access=_create_access_token(payload={**payload.model_dump()}),
        refresh=_create_refresh_token(payload={**payload.model_dump()}),
    )

def decode_access_token(token: str) -> PayloadToken:
    try:
        payload_decoded = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        short_payload = PayloadTokenShort(**payload_decoded)
        return PayloadToken.from_short(short_payload)
    
    except ExpiredSignatureError:
        raise ValueError("Token expired")
    except InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")