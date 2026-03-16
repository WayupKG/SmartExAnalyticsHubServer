from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from app.users.domain.entities import UserEntity
from app.users.domain.enums import UserRole

if TYPE_CHECKING:
    from faker.proxy import Faker


def test_user_entity_creation(faker: Faker) -> None:
    """
    Тест создания сущности пользователя и проверки её полей.
    """
    user_id = 1
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    password = faker.password()
    role = faker.random_element(
        [UserRole.OWNER, UserRole.MARKETER, UserRole.FINANCE],
    )
    user = UserEntity(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        role=role,
        email=email,
        hashed_password=password,
    )

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.role == role
    assert user.email == email
    assert user.hashed_password == password
    assert user.id == user_id
    assert user.is_active is True


def test_user_invalid_email() -> None:
    """
    Пример теста на валидацию, если сущность использует Pydantic.
    """
    with pytest.raises(ValidationError):
        UserEntity(
            email="not-an-email",
            hashed_password="hashed_password",
            role=UserRole.OWNER,
            first_name="John",
            last_name="Doe",
        )
