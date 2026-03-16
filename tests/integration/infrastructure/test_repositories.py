from typing import TYPE_CHECKING

import pytest

from app.users.domain.entities import UserEntity

if TYPE_CHECKING:
    from app.shared.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_user_repository_save_and_get(
    real_uow: SQLAlchemyUnitOfWork,
    random_user: UserEntity,
) -> None:
    """
    Проверка сохранения и получения пользователя через реальный репозиторий.
    """
    await real_uow.users.save(random_user)
    await real_uow.commit()

    result = await real_uow.users.get_by_email(random_user.email)

    assert result is not None
    assert result.email == random_user.email
    assert result.is_active is True
    assert result.id is not None
