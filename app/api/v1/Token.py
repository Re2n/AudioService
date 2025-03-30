from fastapi import APIRouter, Depends

from repositories.User import UserRepository
from services.Auth import AuthService
from core.auth import JWT

auth_service = AuthService(UserRepository())

token_router = APIRouter(prefix="/api/v1", tags=["Token"])


@token_router.get("/get_new_token/")
async def get_new_token(
    payload: dict = Depends(auth_service.get_current_token_payload),
):
    yandex_id = int(payload.get("sub"))
    jwt_payload = {
        "sub": str(yandex_id),
        "email": payload.get("email"),
        "is_superuser": payload.get("is_superuser"),
        "yandex_id": yandex_id,
    }
    token = await JWT.encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "Bearer"}
