from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from app.core.database import db_helper
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.presentation.dependencies import get_uow
from app.users.application.use_cases import RegisterUserUseCase
from app.users.infrastructure.repositories import UserRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_dependency),
    ],
) -> UserRepository:
    return UserRepository(session=session)


async def get_register_user_use_case(
    uow: Annotated[
        IUnitOfWork,
        Depends(get_uow),
    ],
) -> RegisterUserUseCase:
    return RegisterUserUseCase(uow=uow)
