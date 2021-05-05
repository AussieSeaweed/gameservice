from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence, MutableSequence
from typing import TypeVar, Generic, final

from gameframe.exceptions import GameFrameValueError


class GameInterface(ABC):
    """GameInterface is the interface for all games.

       Every game has to define its nature and players.
    """

    @property
    @abstractmethod
    def nature(self) -> ActorInterface:
        """Returns the nature of this game.

        :return: The nature of this game.
        """
        ...

    @property
    @abstractmethod
    def players(self) -> Sequence[ActorInterface]:
        """Returns the players of this game.

        :return: The players of this game.
        """
        ...

    @abstractmethod
    def is_terminal(self) -> bool:
        """Returns the terminal status of this game.

        :return: True if this game is terminal, else False.
        """
        ...


class ActorInterface(ABC):
    """ActorInterface is the interface for all games."""

    @property
    @abstractmethod
    def game(self) -> GameInterface:
        """Returns the game of this actor.

        :return: The game of this actor.
        """
        ...


_G = TypeVar('_G', bound=GameInterface)
_N = TypeVar('_N', bound=ActorInterface)
_P = TypeVar('_P', bound=ActorInterface)


class Game(GameInterface, Generic[_G, _N, _P], ABC):
    """Game is the abstract generic base class for all games."""

    _nature: _N
    _players: MutableSequence[_P]

    @property
    @final
    def nature(self) -> _N:
        return self._nature

    @property
    @final
    def players(self) -> Sequence[_P]:
        return self._players


class Actor(ActorInterface, Generic[_G, _N, _P], ABC):
    """Actor is the abstract base class for all actors."""

    _game: _G

    @property
    @final
    def game(self) -> _G:
        return self._game

    def _act(self) -> None:
        if self.game.is_terminal():
            raise GameFrameValueError('Actions cannot be applied to terminal games')
