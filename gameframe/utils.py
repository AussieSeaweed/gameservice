from typing import List, Sequence, TypeVar

T = TypeVar('T')


def rotate(s: Sequence[T], i: int) -> List[T]:
    return list(s[i:]) + list(s[:i])
