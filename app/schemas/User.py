from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from schemas.Base import Base
from schemas.mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(default=False)
    yandex_id: Mapped[int] = mapped_column(BigInteger)
