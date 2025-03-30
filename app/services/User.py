from sqlalchemy.ext.asyncio import AsyncSession

from models.User import User
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
        return await self.repository.delete(session, user_id)

    async def get_by_yandex_id(self, session: AsyncSession, yandex_id: int):
        return await self.repository.get_by_yandex_id(session, yandex_id)
