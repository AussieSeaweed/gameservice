from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .actions import Action

G = TypeVar('G')
E = TypeVar('E')
N = TypeVar('N')
P = TypeVar('P')


class Log:
    """Log is the class for game action logs.

    Each log instance records information about an action taken in the game and the acting player.
    """

    def __init__(self, action: Action[G, E, N, P]):
        self.__action_str: str = str(action)
        self.__player_str: str = str(action.player)

    def __str__(self) -> str:
        return f'{self.__player_str}: {self.__action_str}'
