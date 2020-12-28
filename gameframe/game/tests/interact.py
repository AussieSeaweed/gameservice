from typing import Any


def pretty_print(o: Any, indent: str = '    ', prefix: str = '') -> None:
    """Prints the object on the console prettily.

    :param o: the object
    :param indent: the indentation string
    :param prefix: the prefix string
    :return: None
    """
    if isinstance(o, list):
        print(prefix + '[')

        for value in o:
            pretty_print(value, indent, prefix + indent)

        print(prefix + ']')
    elif isinstance(o, dict):
        print(prefix + '{')

        for key, value in o.items():
            print(prefix + indent + str(key) + ':')
            pretty_print(value, indent, prefix + indent + indent)

        print(prefix + '}')
    else:
        print(prefix + str(o))
