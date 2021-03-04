from abc import ABC, abstractmethod
from collections import Iterable, Sequence
from typing import Any, Generic, TypeVar, final

from gameframe.exceptions import ActionException


class GameInterface(ABC):
    """GameInterface is the interface for all games.

       Every game has to define its nature and players.
    """

    @property
    @abstractmethod
    def nature(self) -> Any:
        """
        :return: The nature of this game.
        """
        ...

    @property
    @abstractmethod
    def players(self) -> Sequence[Any]:
        """
        :return: The players of this game.
        """
        ...

    @property
    @abstractmethod
    def terminal(self) -> bool:
        """
        :return: True if this game is terminal, else False.
        """
        ...


_N = TypeVar('_N')
_P = TypeVar('_P')


class Game(Generic[_N, _P], GameInterface, ABC):
    """Game is the abstract generic base class for all games."""

    def __init__(self, nature: _N, players: Iterable[_P]):
        self.__nature = nature
        self.__players = tuple(players)

    @property
    @final
    def nature(self) -> _N:
        return self.__nature

    @property
    @final
    def players(self) -> Sequence[_P]:
        return self.__players


_G = TypeVar('_G', bound=GameInterface)
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
        ...
