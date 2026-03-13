from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.shared.domain.exceptions import BaseCustomException
from app.users.application.use_cases import RegisterUserUseCase
from app.users.domain.exceptions import EmailAlreadyExistsError
from app.users.presentation.dependencies import get_register_user_use_case
from app.users.presentation.schemas import UserRegisterRequest, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: UserRegisterRequest,
    use_case: Annotated[
        RegisterUserUseCase,
        Depends(get_register_user_use_case),
    ],
) -> UserResponse | BaseCustomException:
    try:
        user = await use_case.execute(email=request.email, password=request.password)
        return UserResponse(id=user.id, email=user.email, is_active=user.is_active)
    except EmailAlreadyExistsError as e:
        return BaseCustomException(detail=str(e))
