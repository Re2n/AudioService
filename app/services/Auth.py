from fastapi import HTTPException, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from repositories.User import UserRepository
from core.auth import JWT

http_bearer = HTTPBearer()


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_current_token_payload(
        self, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> dict:
        token = credentials.credentials
        try:
            payload = await JWT.decode_jwt(
                token=token,
            )
        except InvalidTokenError as e:
            print(e)
            raise HTTPException(
                status_code=401,
                detail=f"Token invalid",
            )
        return payload
