from datetime import datetime, timedelta

import jwt

from core.config.JWT import auth_jwt


async def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
    expire_minutes: int = auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


async def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
