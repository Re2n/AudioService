from sqlalchemy.ext.asyncio import AsyncSession

from repositories.AudioFile import AudioFileRepository


class AudioFileService:
    def __init__(self, repository: AudioFileRepository):
        self.repository = repository

    async def create(self, session: AsyncSession, owner_id: int, filename: str, filepath: str):
        audio_file = await self.repository.create(session, owner_id, filename, filepath)
        return audio_file

    async def get_by_owner_id(self, session: AsyncSession, owner_id: int):
        audio_files = await self.repository.get_by_owner_id(session, owner_id)
        return audio_files