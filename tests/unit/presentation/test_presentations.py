from typing import TYPE_CHECKING

import pytest
import structlog
from faker.proxy import Faker
from sqlalchemy import select
from starlette import status

from app.users.infrastructure.orm_models import UserModel
from app.users.presentation.schemas import UserReadSchema

if TYPE_CHECKING:
    from httpx import AsyncClient
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.structlog import Logger


logger: Logger = structlog.getLogger(__name__)


@pytest.mark.asyncio
async def test_register_user_api(
    client: AsyncClient, db_session: AsyncSession, faker: Faker
) -> None:
    """
    Тест проверяет эндпоинт регистрации:
    1. Возврат 200 OK и валидной схемы.
    2. Физическое наличие записи в базе данных.
    """
    payload: dict[str, str] = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
    }

    response = await client.post("/api/v1/users/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    user_data = UserReadSchema.model_validate(response.json())
    assert user_data.email == payload["email"]
    assert user_data.is_active is True

    query = select(UserModel).where(UserModel.email == payload["email"])
    result = await db_session.execute(query)
    user_in_db = result.scalar_one_or_none()
    assert user_in_db is not None
    assert user_in_db.email == payload["email"]
    assert user_in_db.hashed_password != payload["password"]
