from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from core.auth.YandexAuth import get_yandex_user
from core.config.Database import db, env
from models.User import User, UserResponse, UserUpdate
from repositories.User import UserRepository
from services.Auth import AuthService
from services.User import UserService
from core.auth import JWT

user_router = APIRouter(tags=["User"])
user_service = UserService(UserRepository())
auth_service = AuthService(UserRepository())


@user_router.get("/auth/yandex/")
async def login_via_yandex(
    code: str, session: Annotated[AsyncSession, Depends(db.session_getter)]
):
    yandex_user = await get_yandex_user(code)
    yandex_id = int(yandex_user.get("id"))
    email = yandex_user.get("default_email")
    user = await user_service.get_by_yandex_id(session, yandex_id)
    if not user:
        user_create = User(
            email=email,
            yandex_id=yandex_id,
        )
        await user_service.create_user(session, user_create)
    user = await user_service.get_by_yandex_id(session, yandex_id)
    jwt_payload = {
        "sub": str(yandex_id),
        "email": email,
        "is_superuser": user.is_superuser,
        "yandex_id": yandex_id,
    }
    token = await JWT.encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "Bearer"}

@user_router.get("/get_user/{user_id}")
async def get_user(user_id: int,
                   session: Annotated[AsyncSession, Depends(db.session_getter)],
                    payload: dict = Depends(auth_service.get_current_token_payload)
):
    is_superuser = payload.get("is_superuser")
    if is_superuser:
        user = await user_service.get_by_user_id(session, user_id)
        return UserResponse(id=user.id, email=user.email, is_superuser=user.is_superuser, yandex_id=user.yandex_id)
    raise HTTPException(
        status_code=403,
        detail="Error access denied",
    )

@user_router.patch("/update_user/{user_id}")
async def update_user(user_id: int,
                      user_update: UserUpdate,
                      session: Annotated[AsyncSession, Depends(db.session_getter)],
                      payload: dict = Depends(auth_service.get_current_token_payload)
):
    is_superuser = payload.get("is_superuser")
    if is_superuser:
        user = await user_service.update(session, user_id, user_update)
        return UserResponse(id=user.id, email=user.email, is_superuser=user.is_superuser, yandex_id=user.yandex_id)
    raise HTTPException(
        status_code=403,
        detail="Error access denied",
    )



@user_router.delete("/delete_user/{user_id}/")
async def delete_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    payload: dict = Depends(auth_service.get_current_token_payload),
):
    is_superuser = payload.get("is_superuser")
    if is_superuser:
        user = await user_service.delete_user(session, user_id)
        return UserResponse(id=user.id, email=user.email, is_superuser=user.is_superuser, yandex_id=user.yandex_id)
    raise HTTPException(
        status_code=403,
        detail="Error access denied",
    )


@user_router.get("/auth/redirect_to_auth_url/")
async def redirect_url():
    return RedirectResponse(
        f"https://oauth.yandex.ru/authorize?response_type=code&client_id={env.YANDEX_CLIENT_ID}"
    )
