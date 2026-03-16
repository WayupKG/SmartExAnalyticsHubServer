import pytest

from app.shared.infrastructure.security import validate_password
from app.users.application.use_cases import RegisterUserUseCase
from app.users.domain.entities import UserEntity
from app.users.domain.exceptions import EmailAlreadyExistsError
from app.users.presentation.schemas import UserCreateSchema
from tests.fixtures.factories.user_factory import UserFactory
from tests.fixtures.fakes.fake_uow import FakeUnitOfWork


@pytest.mark.asyncio
async def test_create_user_use_case_success(random_user: UserEntity) -> None:
    """
    Проверка успешного создания пользователя через Use Case.
    """
    uow = FakeUnitOfWork()
    use_case = RegisterUserUseCase(uow=uow)

    user = await use_case.execute(
        user_in=UserCreateSchema(
            first_name=random_user.first_name,
            last_name=random_user.last_name,
            email=random_user.email,
            password=random_user.hashed_password,
        )
    )

    assert user.email == random_user.email
    assert validate_password(
        password=random_user.hashed_password,
        hashed_password=user.hashed_password,
    )
    assert uow.committed is True


@pytest.mark.asyncio
async def test_create_user_use_case_already_exists(user_factory: UserFactory) -> None:
    """
    Тест логики, когда пользователь с таким email уже есть.
    """
    uow = FakeUnitOfWork()

    user1: UserEntity = user_factory.build()

    await uow.users.save(user1)

    use_case = RegisterUserUseCase(uow=uow)

    with pytest.raises(EmailAlreadyExistsError) as exc_info:
        await use_case.execute(
            user_in=UserCreateSchema(
                first_name=user1.first_name,
                last_name=user1.last_name,
                email=user1.email,
                password=user1.hashed_password,
            )
        )

    assert uow.committed is False
