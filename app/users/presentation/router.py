from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.users.application.use_cases import RegisterUserUseCase
from app.users.presentation.dependencies import get_register_user_use_case
from app.users.presentation.schemas import UserCreateSchema, UserReadSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: UserCreateSchema,
    use_case: Annotated[
        RegisterUserUseCase,
        Depends(get_register_user_use_case),
    ],
) -> UserReadSchema:
    user = await use_case.execute(user_in=request)
    return UserReadSchema.model_validate(user)
