from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.User import UserUpdate
from schemas.User import User


class UserRepository:
    model = User

    async def create(
        self,
        session: AsyncSession,
        email: EmailStr,
        yandex_id: int,
        is_superuser: bool = False,
    ):
        new_user = self.model(
            email=email, is_superuser=is_superuser, yandex_id=yandex_id
        )
        session.add(new_user)
        await session.commit()
        return new_user

    async def delete(self, session: AsyncSession, user_id: int):
        stmt = select(self.model).where(self.model.id == user_id)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
        return user

    async def get_by_yandex_id(self, session: AsyncSession, yandex_id: int):
        stmt = select(self.model).where(self.model.yandex_id == yandex_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_user_id(self, session: AsyncSession, user_id: int):
        stmt = select(self.model).where(self.model.id == user_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(
        self, session: AsyncSession, user_id: int, user_update: UserUpdate
    ):
        user = await self.get_by_user_id(session, user_id)
        if user is None:
            return user

        user_dict = user_update.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in user_dict.items():
            setattr(user, field, value)

        session.add(user)
        await session.commit()
        return user
