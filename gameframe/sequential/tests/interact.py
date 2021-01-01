from typing import Callable

from gameframe.game import Action, Environment, Game, Nature, Player
from gameframe.game.tests import pretty_print
from gameframe.sequential import SequentialGame


def interact_sequential(sequential_game_factory: Callable[[], SequentialGame]) -> None:
    """Interacts with sequential games on the console.

    :param sequential_game_factory: a function that creates a sequential game instance
    :return: None
    """
    sequential_game: SequentialGame = sequential_game_factory()

    while not sequential_game.terminal:
        pretty_print(sequential_game.actor.information_set)

        actions: list[Action[Game, Environment, Nature, Player]] = sequential_game.actor.actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    pretty_print(sequential_game.nature.information_set)
