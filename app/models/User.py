from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    is_superuser: bool = False
    yandex_id: int


class UserResponse(BaseModel):
    id: int
    email: EmailStr
