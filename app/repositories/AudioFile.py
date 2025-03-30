from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.AudioFile import AudioFile as AudioFileSchema


class AudioFileRepository:
    model = AudioFileSchema

    async def create(
        self, session: AsyncSession, owner_id: int, filename: str, filepath: str
    ):
        new_audio_file = self.model(
            filename=filename, file_path=filepath, owner_id=owner_id
        )
        session.add(new_audio_file)
        await session.commit()
        return new_audio_file

    async def get_by_owner_id(self, session: AsyncSession, owner_id: int):
        stmt = select(self.model).where(self.model.owner_id == owner_id)
        res = await session.execute(stmt)
        return res.scalars().all()
