from datetime import UTC, datetime, timedelta
from typing import Any

from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from app.core.config import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
    expires_minutes: float = settings.jwt.access_token_expire_minutes,
    expires_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expires_timedelta:
        expires = now + expires_timedelta
    else:
        expires = now + timedelta(minutes=expires_minutes)
    to_encode.update(
        exp=expires,
        iat=now,
    )
    return jwt_encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> Any:
    return jwt_decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
