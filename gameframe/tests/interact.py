from typing import Any, Callable

from gameframe.game import Action
from gameframe.sequential import SequentialGame
from gameframe.tictactoe import TicTacToeGame


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


def sequential_interact(sequential_game_factory: Callable[[], SequentialGame]) -> None:
    """Interacts with sequential games on console.

    :param sequential_game_factory: a function that creates a sequential game instance
    :return: None
    """
    sequential_game: SequentialGame = sequential_game_factory()

    while not sequential_game.terminal:
        pretty_print(sequential_game.actor.information_set)

        actions: list[Action] = sequential_game.actor.actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    pretty_print(sequential_game.nature.information_set)


def main():
    sequential_interact(TicTacToeGame)


if __name__ == '__main__':
    main()
