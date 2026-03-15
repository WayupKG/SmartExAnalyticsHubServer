import uuid

from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserReadSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
