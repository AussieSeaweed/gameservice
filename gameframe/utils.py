from typing import Sequence, TypeVar

T = TypeVar('T')


def rotate(s: Sequence[T], i: int) -> Sequence[T]:
    return list(s[i:]) + list(s[:i])
