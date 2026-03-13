import hashlib
import secrets

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
