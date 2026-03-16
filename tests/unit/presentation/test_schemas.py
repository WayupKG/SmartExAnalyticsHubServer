from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from app.users.domain.entities import UserEntity
from app.users.presentation.schemas import UserCreateSchema, UserReadSchema

if TYPE_CHECKING:
    from faker.proxy import Faker


def test_user_create_schema_valid(faker: Faker) -> None:
    """Проверка создания схемы с валидными данными."""
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": faker.password(),
    }
    schema = UserCreateSchema(**data)

    assert schema.email == data["email"]
    assert str(schema.password) == data["password"]


def test_user_create_invalid_email(random_user: UserEntity) -> None:
    """Проверка валидации некорректного email."""
    random_user.email = "invalid-email"
    with pytest.raises(ValidationError) as exc_info:
        UserReadSchema.model_validate(random_user)
