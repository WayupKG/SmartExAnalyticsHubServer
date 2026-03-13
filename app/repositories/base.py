from typing import TYPE_CHECKING, Any

from sqlalchemy import ColumnElement, and_, or_, select

from app.enums.filters import Op

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm.interfaces import ORMOption
    from sqlalchemy.sql.selectable import Select

    from app.database.models import Base
    from app.filters.expressions import Condition


class BaseSQLAlchemyRepository:
    model: type[Base]

    def condition_to_expression(self, condition: Condition) -> ColumnElement[bool]:
        if condition.op == Op.AND:
            return and_(
                *[self.condition_to_expression(child) for child in condition.children]
            )
        if condition.op == Op.OR:
            return or_(
                *[self.condition_to_expression(child) for child in condition.children]
            )

        if not condition.field:
            raise ValueError(f"Unsupported condition: {condition}")

        column = getattr(self.model, condition.field)

        # Маппинг операторов для устранения веток if/match
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
        return operation(column, condition.value)

    def _get_statement(
        self,
        filters: Condition | None = None,
        options: Sequence[ORMOption] | None = None,
    ) -> Select[tuple[Base]]:
        stmt = select(self.model)
        if options:
            stmt = stmt.options(*options)
        if filters:
            query_filter = self.condition_to_expression(condition=filters)
            stmt = stmt.filter(query_filter)
        return stmt

    def _apply_updates(self, obj: Base, update_data: dict[str, Any]) -> None:
        for key, value in update_data.items():
            if not hasattr(obj, key):
                raise AttributeError(f"{self.model.__name__} has no attribute '{key}'")
            setattr(obj, key, value)


class SQLAlchemyRepository(BaseSQLAlchemyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, data: dict[str, Any]):
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def find_one_by(
        self,
        filters: Condition,
        options: Sequence[ORMOption] | None = None,
    ):
        stmt = self._get_statement(filters=filters, options=options)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_by(
        self,
        filters: Condition,
        limit: int | None = None,
        offset: int | None = None,
    ):
        stmt = self._get_statement(filters=filters)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_all(
        self,
        limit: int,
        offset: int,
    ):
        stmt = select(self.model)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_partial_by_filter(
        self,
        filters: Condition,
        update_data: dict[str, Any],
    ):
        stmt = self._get_statement(filters=filters)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()
        if not obj:
            return None
        self._apply_updates(obj, update_data)
        await self.session.flush()
        return obj

    async def delete_by_filter(
        self,
        filters: Condition,
    ):
        stmt = self._get_statement(filters=filters)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()
        if not obj:
            return None
        await self.session.delete(obj)
        return obj
