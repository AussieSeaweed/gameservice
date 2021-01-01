from typing import TypeVar

T = TypeVar('T')


def rotate(collection: list[T], index: int) -> list[T]:
    """Rotates the list by an index.

    :param collection: the list to be rotated
    :param index: the index of rotation
    :return: the rotated list
    """
    return collection[index:] + collection[:index]
