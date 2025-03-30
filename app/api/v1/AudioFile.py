import os
import uuid
from typing import Annotated

import magic
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from core.config.Database import db
from models.AudioFile import AudioFile
from repositories.AudioFile import AudioFileRepository
from repositories.User import UserRepository
from services.AudioFile import AudioFileService
from services.Auth import AuthService

audio_file_router = APIRouter(tags=['Audio file'])
auth_service = AuthService(UserRepository())
audio_file_service = AudioFileService(AudioFileRepository())

@audio_file_router.post('/upload_audio_file/')
async def audio_file_upload(
        filename: str,
        session: Annotated[AsyncSession, Depends(db.session_getter)],
        file: UploadFile = File(...),
        payload: dict = Depends(auth_service.get_current_token_payload),
):
    mime = magic.Magic(mime=True)
    file_content = await file.read()
    mime_type = mime.from_buffer(file_content)
    if not mime_type.startswith('audio/'):
        raise HTTPException(
            status_code=400,
            detail="Загруженный файл не является аудиофайлом"
        )
    await file.seek(0)
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_location = f"static/{unique_filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    user = await auth_service.get_current_auth_user(session, payload)
    audio_file = await audio_file_service.create(session, user.id, filename, str(file_location))
    return AudioFile(filename=audio_file.filename, file_path=audio_file.file_path)

@audio_file_router.get("/get_audio_files/")
async def get_audio_files(
        session: Annotated[AsyncSession, Depends(db.session_getter)],
        payload: dict = Depends(auth_service.get_current_token_payload),
):
    user = await auth_service.get_current_auth_user(session, payload)
    audio_files = await audio_file_service.get_by_owner_id(session, user.id)
    return [
        AudioFile(filename=file.filename, file_path=file.file_path)
        for file in audio_files
    ]
