from typing import TYPE_CHECKING, cast

import pytest

from tests.fixtures.factories.user_factory import UserFactory

if TYPE_CHECKING:
    from app.users.domain.entities import UserEntity


@pytest.fixture
def user_factory() -> type[UserFactory]:
    """Фикстура, возвращающая класс фабрики для создания сущностей."""
    return UserFactory


@pytest.fixture
def random_user(user_factory: type[UserFactory]) -> UserEntity:
    return cast("UserEntity", user_factory.build())
