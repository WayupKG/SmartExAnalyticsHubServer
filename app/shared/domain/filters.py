from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any

from app.shared.domain.enums import Op


@dataclass(frozen=True)
class Condition:
    """
    Неизменяемый (frozen) класс для построения спецификаций запросов.
    """

    op: Op
    field: str | None = None
    value: Any = None

    # Используем алиас, чтобы не конфликтовать с атрибутом field
    children: list[Condition] = dataclass_field(default_factory=list)

    def __repr__(self) -> str:
        if self.op in {Op.AND, Op.OR}:
            return f"{self.op.name.upper()}({', '.join(map(str, self.children))})"
        return f"{self.field} {self.op.name} {self.value}"

    @staticmethod
    def eq(field: str, value: Any) -> Condition:
        return Condition(op=Op.EQ, field=field, value=value)

    @staticmethod
    def ne(field: str, value: Any) -> Condition:
        return Condition(op=Op.NE, field=field, value=value)

    @staticmethod
    def gt(field: str, value: Any) -> Condition:
        return Condition(op=Op.GT, field=field, value=value)

    @staticmethod
    def lt(field: str, value: Any) -> Condition:
        return Condition(op=Op.LT, field=field, value=value)

    @staticmethod
    def ge(field: str, value: Any) -> Condition:
        return Condition(op=Op.GE, field=field, value=value)

    @staticmethod
    def le(field: str, value: Any) -> Condition:
        return Condition(op=Op.LE, field=field, value=value)

    @staticmethod
    def in_(field: str, value: list[Any]) -> Condition:
        return Condition(op=Op.IN, field=field, value=value)

    @staticmethod
    def like(field: str, value: str) -> Condition:
        return Condition(op=Op.LIKE, field=field, value=value)

    @staticmethod
    def ilike(field: str, value: str) -> Condition:
        return Condition(op=Op.ILIKE, field=field, value=value)

    @staticmethod
    def and_(*conditions: Condition) -> Condition:
        return Condition(op=Op.AND, children=list(conditions))

    @staticmethod
    def or_(*conditions: Condition) -> Condition:
        return Condition(op=Op.OR, children=list(conditions))
