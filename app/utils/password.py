from typing import TYPE_CHECKING

import bcrypt
import structlog

if TYPE_CHECKING:
    from app.core.structlog import Logger

logger: Logger = structlog.getLogger(__name__)


def hash_password(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    hashpw = bcrypt.hashpw(password.encode(), salt)
    return hashpw.decode()


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except ValueError as e:
        logger.error(f"Ошибка проверки пароля: {e}")
        return False
