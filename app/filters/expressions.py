from typing import Any

from app.enums import Op


class Condition:
    def __init__(
        self,
        op: Op,
        field: str | None = None,
        value: Any = None,
        children: list[Condition] | None = None,
    ):
        self.op = op
        self.field = field
        self.value = value
        self.children = children or []

    def __repr__(self) -> str:
        if self.op in {Op.AND, Op.OR}:
            return f"{self.op.upper()}({', '.join(map(str, self.children))})"
        return f"{self.field} {self.op} {self.value}"

    @staticmethod
    def eq(field: str, value: Any) -> Condition:
        return Condition(Op.EQ, field, value)

    @staticmethod
    def ne(field: str, value: Any) -> Condition:
        return Condition(Op.NE, field, value)

    @staticmethod
    def gt(field: str, value: Any) -> Condition:
        return Condition(Op.GT, field, value)

    @staticmethod
    def lt(field: str, value: Any) -> Condition:
        return Condition(Op.LT, field, value)

    @staticmethod
    def ge(field: str, value: Any) -> Condition:
        return Condition(Op.GE, field, value)

    @staticmethod
    def le(field: str, value: Any) -> Condition:
        return Condition(Op.LE, field, value)

    @staticmethod
    def in_(field: str, value: list[Any]) -> Condition:
        return Condition(Op.IN, field, value)

    @staticmethod
    def like(field: str, value: str) -> Condition:
        return Condition(Op.LIKE, field, value)

    @staticmethod
    def ilike(field: str, value: str) -> Condition:
        return Condition(Op.ILIKE, field, value)

    @staticmethod
    def and_(*conditions: Condition) -> Condition:
        return Condition(Op.AND, children=list(conditions))

    @staticmethod
    def or_(*conditions: Condition) -> Condition:
        return Condition(Op.OR, children=list(conditions))
