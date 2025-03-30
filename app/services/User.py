from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.User import User, UserUpdate
from repositories.User import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, session: AsyncSession, user: User):
        return await self.repository.create(
            session,
            email=user.email,
            is_superuser=user.is_superuser,
            yandex_id=user.yandex_id,
        )

    async def delete_user(self, session: AsyncSession, user_id: int):
        user = await self.repository.delete(session, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_by_yandex_id(self, session: AsyncSession, yandex_id: int):
        return await self.repository.get_by_yandex_id(session, yandex_id)

    async def get_by_user_id(self, session: AsyncSession, user_id: int):
        user = await self.repository.get_by_user_id(session, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update(
        self, session: AsyncSession, user_id: int, user_update: UserUpdate
    ):
        user = await self.repository.update(session, user_id, user_update)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
