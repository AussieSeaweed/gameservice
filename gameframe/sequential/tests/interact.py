from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from gameframe.utils import pretty_print

if TYPE_CHECKING:
    from gameframe.game import Action
    from gameframe.sequential import SequentialGame

__all__: Sequence[str] = ['interact_sequential']


def interact_sequential(sequential_game_factory: Callable[[], SequentialGame]) -> None:
    """Interacts with a sequential game on the console.

    :param sequential_game_factory: a function that creates the sequential game instance
    :return: None
    """
    sequential_game: SequentialGame = sequential_game_factory()

    while not sequential_game.terminal:
        pretty_print(sequential_game.actor.information_set)

        actions: Sequence[Action] = sequential_game.actor.actions

        actions[0 if len(actions) == 1 else int(input('Action #: '))].act()

    pretty_print(sequential_game.nature.information_set)
