from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from typing import Generic, TypeVar, cast, final

from gameframe.exceptions import GameFrameError


class BaseGame(ABC):
    """BaseGame is the base abstract class for all games.

    Every game has to define its nature and players.
    """

    @property
    @abstractmethod
    def nature(self) -> BaseActor:
        """Returns the nature of this game.

        :return: The nature of this game.
        """
        ...

    @property
    @abstractmethod
    def players(self) -> Sequence[BaseActor]:
        """Returns the players of this game.

        :return: The players of this game.
        """
        ...

    @property
    @abstractmethod
    def terminal(self) -> bool:
        """Returns the terminal status of this game.

        :return: True if this game is terminal, else False.
        """
        ...


class BaseActor(ABC):
    """BaseActor is the base abstract class for all games."""

    @property
    @abstractmethod
    def game(self) -> BaseGame:
        """Returns the game of this actor.

        :return: The game of this actor.
        """
        ...


_G = TypeVar('_G', bound=BaseGame)
_N = TypeVar('_N', bound=BaseActor)
_P = TypeVar('_P', bound=BaseActor)
_A = TypeVar('_A', bound=BaseActor)


class Game(BaseGame, Generic[_N, _P], ABC):
    """Game is the abstract class for all games.

    :param nature: The nature of this game.
    :param players: The players of this game.
    """

    def __init__(self, nature: _N, players: Iterable[_P]):
        self._nature = nature
        self._players = list(players)

    @property
    @final
    def nature(self) -> _N:
        return self._nature

    @property
    @final
    def players(self) -> Sequence[_P]:
        return self._players


class Actor(BaseActor, Generic[_G]):
    """Actor is the class for actors.

    :param game: The game of this actor.
    """

    def __init__(self, game: _G):
        self._game = game

    @property
    @final
    def game(self) -> _G:
        return self._game


class _Action(Generic[_G, _A]):
    def __init__(self, actor: _A):
        self.actor = actor

    @property
    def game(self) -> _G:
        return cast(_G, self.actor.game)

    def act(self) -> None:
        self.verify()
        self.apply()

    def can_act(self) -> bool:
        try:
            self.verify()
        except GameFrameError:
            return False
        else:
            return True

    def verify(self) -> None:
        if self.game.terminal:
            raise GameFrameError('Actions cannot be applied to terminal games')

    def apply(self) -> None:
        ...
