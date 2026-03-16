import enum


class UserRole(enum.StrEnum):
    OWNER = "owner"  # Владелец компании
    MARKETER = "marketer"  # Маркетолог
    FINANCE = "finance"  # Финансы
