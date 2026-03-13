from enum import StrEnum


class Op(StrEnum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    LT = "lt"
    GE = "ge"
    LE = "le"
    IN = "in"
    LIKE = "like"
    ILIKE = "ilike"
    AND = "and"
    OR = "or"
