from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from schemas.Base import Base
from schemas.mixins.int_id_pk import IntIdPkMixin


class AudioFile(Base, IntIdPkMixin):
    __tablename__ = "audio_files"

    filename: Mapped[str] = mapped_column(index=True)
    file_path: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
