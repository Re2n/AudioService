from fastapi import HTTPException, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from models.User import UserResponse
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

    async def get_current_auth_user(
        self,
        session: AsyncSession,
        payload: dict = Depends(get_current_token_payload),
    ) -> UserResponse:
        yandex_id = int(payload.get("sub"))
        res = await self.repository.get_by_yandex_id(session, yandex_id)
        if res is not None:
            return UserResponse(
                id=res.id,
                email=res.email,
                is_superuser=res.is_superuser,
                yandex_id=res.yandex_id,
            )

        raise HTTPException(
            status_code=401,
            detail="Token invalid",
        )
