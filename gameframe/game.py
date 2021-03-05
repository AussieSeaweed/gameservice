from abc import ABC, abstractmethod
from collections import Iterable, Sequence
from typing import Any, Generic, TypeVar, final

from gameframe.exceptions import ActionException

_N = TypeVar('_N')
_P = TypeVar('_P')


class Game(Generic[_N, _P], ABC):
    """Game is the abstract generic base class for all games.

       Every game has to define its nature and players.
    """

    def __init__(self, nature: _N, players: Iterable[_P]):
        self.__nature = nature
        self.__players = tuple(players)

    @property
    @final
    def nature(self) -> _N:
        """
        :return: The nature of this game.
        """
        return self.__nature

    @property
    @final
    def players(self) -> Sequence[_P]:
        """
        :return: The players of this game.
        """
        return self.__players

    @property
    @abstractmethod
    def terminal(self) -> bool:
        """
        :return: True if this game is terminal, else False.
        """
        pass


_G = TypeVar('_G', bound=Game[Any, Any])
_A = TypeVar('_A')


class _Action(Generic[_G, _A], ABC):
    def __init__(self, game: _G, actor: _A):
        self.game = game
        self.actor = actor

    def act(self) -> None:
        self.verify()
        self.apply()

    def verify(self) -> None:
        if self.game.terminal:
            raise ActionException('Actions cannot be applied to terminal games')

    @abstractmethod
    def apply(self) -> None:
        pass
