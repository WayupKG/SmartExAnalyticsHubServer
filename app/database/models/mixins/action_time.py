from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from datetime import datetime


class ActionDataTime:
    """
    Class to represent action data timestamps.

    Attributes:
    -----------
    created_at : Mapped[datetime]
        Timestamp indicating when the entry was created.
        Uses the current time as the default
        value and is not nullable.

    updated_at : Mapped[datetime]
        Timestamp indicating when the entry was last updated.
        Uses the current time as the default
        value and updates to the current time on update.
        Nullable.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=True,
    )
