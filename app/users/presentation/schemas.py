from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.users.domain.enums import UserRole


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserReadSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: UserRole
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
