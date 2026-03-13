import hashlib
import secrets
from dataclasses import dataclass

MAX_ALLOWED_ZERO_DIGITS = 2


def six_digit_with_max_two_zeros() -> int:
    while True:
        num = secrets.randbelow(900000) + 100000
        if str(num).count("0") <= MAX_ALLOWED_ZERO_DIGITS:
            return num


def generate_hash(data: str) -> str:
    byte_data = data.encode("utf-8")
    hash_object = hashlib.sha256(byte_data)
    return hash_object.hexdigest()


def build_charset(size: int = 200) -> str:
    """
    Формирует строку из `size` китайских иероглифов,
    начиная с диапазона CJK Unified Ideographs (0x4E00).
    """
    base = 0x4E00
    return "".join(chr(base + i) for i in range(size))


@dataclass(frozen=True)
class NicknameGenerator:
    charset: str = build_charset(200)

    def __post_init__(self):
        base = len(self.charset)
        object.__setattr__(self, "base", base)
        object.__setattr__(self, "capacity", base**3)

    def from_index(self, index: int) -> str:
        """
        Преобразует целое число в уникальный ник из 3 иероглифов.

        index должен быть < base^3.
        """
        if index < 0:
            raise ValueError("index должен быть >= 0")

        if index >= self.capacity:
            raise ValueError(
                f"index={index} превышает максимум capacity={self.capacity}"
            )

        b = self.base

        # Разложение числа в систему счисления base^3
        i1 = index // (b * b)
        i2 = (index // b) % b
        i3 = index % b

        return self.charset[i1] + self.charset[i2] + self.charset[i3]


nickname_gen = NicknameGenerator()
