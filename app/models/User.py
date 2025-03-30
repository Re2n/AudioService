from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    is_superuser: bool = False
    yandex_id: int


class UserResponse(User):
    id: int


class UserUpdate(BaseModel):
    email: str | None = None
    is_superuser: bool | None = None
    yandex_id: int | None = None
