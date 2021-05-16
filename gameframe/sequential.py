from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TypeVar, final

from gameframe.exceptions import GameFrameValueError
from gameframe.game import Actor, BaseActor, BaseGame, Game, _Action


class BaseSequentialGame(BaseGame, ABC):
    """BaseSequentialGame is the base abstract class for all sequential games.

       In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game
       is terminal, its actor attribute must be set to None to denote such.
    """

    @property
    @abstractmethod
    def actor(self) -> Optional[BaseSequentialActor]:
        """Returns the current actor of this sequential game.

        :return: The current actor of this sequential game.
        """
        ...

    @property
    @final
    def terminal(self) -> bool:
        return self.actor is None


class BaseSequentialActor(BaseActor, ABC):
    """BaseSequentialActor is the base abstract class for all sequential actors."""

    @property
    @abstractmethod
    def game(self) -> BaseSequentialGame: ...


_G = TypeVar('_G', bound=BaseSequentialGame)
_N = TypeVar('_N', bound=BaseSequentialActor)
_P = TypeVar('_P', bound=BaseSequentialActor)
_A = TypeVar('_A', bound=BaseSequentialActor)


class SequentialGame(Game[_G, _N, _P], BaseSequentialGame, ABC):
    """SequentialGame is the abstract class for all sequential games."""

    _actor: Optional[BaseSequentialActor]

    @property
    @final
    def actor(self) -> Optional[BaseSequentialActor]:
        return self._actor


class SequentialActor(Actor[_G, _N, _P], BaseSequentialActor, ABC):
    """SequentialActor is the abstract class for all sequential actors."""
    ...


class _SequentialAction(_Action[_A], ABC):
    def verify(self) -> None:
        super().verify()

        if self.actor.game.actor is not self.actor:
            raise GameFrameValueError('The actor is not in turn')
