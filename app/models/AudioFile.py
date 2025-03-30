from pydantic import BaseModel


class AudioFile(BaseModel):
    filename: str
    file_path: str