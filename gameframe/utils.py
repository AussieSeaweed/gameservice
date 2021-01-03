from typing import Any, Callable, Sequence, TypeVar

C = TypeVar('C', bound=Callable)
T = TypeVar('T')


def override(function: C) -> C:
    """Annotates the function that it overrides the super class's definition

    :param function: the overriding function
    :return: the overriding function
    """
    return function


def pretty_print(o: Any, indent: str = '    ', start: str = '', end: str = '\n') -> None:
    """Prints the object on the console prettily.

    :param o: the object
    :param indent: the indentation string
    :param start: the prefix string
    :param end: the suffix string
    :return: None
    """
    if isinstance(o, list):
        print(start + '[')

        for value in o:
            pretty_print(value, indent, start + indent, end=',\n')

        print(start + ']', end=end)
    elif isinstance(o, dict):
        print(start + '{')

        for key, value in o.items():
            print(start + indent + str(key), end=':\n')
            pretty_print(value, indent, start + indent + indent, end=',\n')

        print(start + '}', end=end)
    else:
        print(start + str(o), end=end)


def rotate(collection: Sequence[T], index: int) -> Sequence[T]:
    """Rotates the sequence by an index.

    :param collection: the sequence to be rotated
    :param index: the index of rotation
    :return: the rotated sequence
    """
    return list(collection[index:]) + list(collection[:index])
