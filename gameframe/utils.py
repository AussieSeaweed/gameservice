from collections import Sequence
from typing import TypeVar

T = TypeVar('T')


def rotate(s: Sequence[T], i: int) -> list[T]:
    return list(s[i:]) + list(s[:i])
