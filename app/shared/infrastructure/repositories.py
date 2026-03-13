from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    cast,
)

from sqlalchemy import ColumnElement, and_, or_, select
from sqlalchemy.exc import MultipleResultsFound

from app.shared.domain.enums import Op
from app.shared.infrastructure.orm_base import Base

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.interfaces import ORMOption
    from sqlalchemy.sql.selectable import Select

    from app.shared.domain.filters import Condition


ModelType = TypeVar("ModelType", bound=Base)


class BaseSQLAlchemyRepository(Generic[ModelType]):
    model: type[ModelType]

    def condition_to_expression(self, condition: Condition) -> ColumnElement[bool]:
        if condition.op == Op.AND:
            return and_(*[self.condition_to_expression(c) for c in condition.children])
        if condition.op == Op.OR:
            return or_(*[self.condition_to_expression(c) for c in condition.children])

        if not condition.field:
            raise ValueError(f"Unsupported condition: {condition}")

        column = getattr(self.model, condition.field)

        operators: dict[Op, Callable[[Any, Any], Any]] = {
            Op.EQ: lambda col, val: col == val,
            Op.NE: lambda col, val: col != val,
            Op.GT: lambda col, val: col > val,
            Op.LT: lambda col, val: col < val,
            Op.GE: lambda col, val: col >= val,
            Op.LE: lambda col, val: col <= val,
            Op.IN: lambda col, val: col.in_(val),
            Op.LIKE: lambda col, val: col.like(val),
            Op.ILIKE: lambda col, val: col.ilike(val),
        }

        operation = operators.get(condition.op)
        if not operation:
            raise ValueError(f"Unsupported operation: {condition.op}")
        return cast("ColumnElement[bool]", operation(column, condition.value))

    def _get_statement(
        self,
        filters: Condition | None = None,
        options: Sequence[ORMOption] | None = None,
    ) -> Select[tuple[ModelType]]:
        stmt = select(self.model)
        if options:
            stmt = stmt.options(*options)
        if filters:
            query_filter = self.condition_to_expression(condition=filters)
            stmt = stmt.filter(query_filter)
        return stmt

    def _apply_updates(self, obj: ModelType, update_data: dict[str, Any]) -> None:
        for key, value in update_data.items():
            if not hasattr(obj, key):
                raise AttributeError(
                    f"Model '{self.model.__name__}' has no attribute '{key}'"
                )
            setattr(obj, key, value)


class SQLAlchemyRepository(BaseSQLAlchemyRepository[ModelType]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, obj: ModelType) -> ModelType:
        """
        Добавляет уже созданный ORM-объект в сессию.
        """
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get_one(
        self,
        filters: Condition,
        options: Sequence[ORMOption] | None = None,
    ) -> ModelType | None:
        """
        Строгий поиск одной записи.
        Выбросит ошибку, если под фильтр попадет больше одной записи.
        """
        stmt = self._get_statement(filters=filters, options=options)
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one_or_none()
        except MultipleResultsFound as err:
            raise ValueError(
                f"Ожидалась одна запись {self.model.__name__}, но найдено несколько."
            ) from err

    async def find(
        self,
        filters: Condition,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[ModelType]:
        """Поиск множества записей по фильтру."""
        stmt = self._get_statement(filters=filters)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[ModelType]:
        """Получение всех записей с возможной пагинацией."""
        stmt = select(self.model)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(
        self,
        filters: Condition,
        update_data: dict[str, Any],
    ) -> ModelType | None:
        """
        Частичное обновление единственной записи по фильтру.
        Выбросит ошибку, если под фильтр попадет больше одной записи.
        """
        stmt = self._get_statement(filters=filters)
        result = await self.session.execute(stmt)

        try:
            obj = result.scalar_one_or_none()
        except MultipleResultsFound as err:
            raise ValueError(
                f"Ожидалась одна запись {self.model.__name__} для обновления, "
                f"но найдено несколько. Обновление прервано для защиты данных."
            ) from err

        if not obj:
            return None

        self._apply_updates(obj, update_data)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(
        self,
        filters: Condition,
    ) -> ModelType | None:
        """Удаляет первую найденную запись."""
        stmt = self._get_statement(filters=filters)
        result = await self.session.execute(stmt)
        try:
            obj = result.scalar_one_or_none()
        except MultipleResultsFound as err:
            raise ValueError(
                f"Ожидалась одна запись {self.model.__name__} для удаление, "
                f"но найдено несколько. Обновление прервано для защиты данных."
            ) from err

        if not obj:
            return None

        await self.session.delete(obj)
        await self.session.flush()
        return obj
