from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TypeVar, final

from gameframe.exceptions import GameFrameValueError
from gameframe.game import Game, GameInterface, ActorInterface, Actor


class SequentialGameInterface(GameInterface, ABC):
    """SequentialGameInterface is the interface for all sequential games.

       In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game
       is terminal, its actor attribute must be set to None to denote such.
    """

    @property
    @abstractmethod
    def actor(self) -> Optional[SequentialActorInterface]:
        """Returns the current actor of this sequential game.

        :return: The current actor of this sequential game.
        """
        ...

    @final
    def is_terminal(self) -> bool:
        return self.actor is None


class SequentialActorInterface(ActorInterface, ABC):
    """SequentialActorInterface is the interface for all sequential actors."""
    ...


_G = TypeVar('_G', bound=SequentialGameInterface)
_N = TypeVar('_N', bound=SequentialActorInterface)
_P = TypeVar('_P', bound=SequentialActorInterface)


class SequentialGame(Game[_G, _N, _P], SequentialGameInterface, ABC):
    """SequentialGame is the abstract generic base class for all sequential games."""

    _actor: Optional[SequentialActorInterface]

    @property
    @final
    def actor(self) -> Optional[SequentialActorInterface]:
        return self._actor


class SequentialActor(Actor[_G, _N, _P], SequentialActorInterface, ABC):
    """SequentialActor is the abstract generic base class for all sequential actors."""

    def _act(self) -> None:
        super()._act()

        if self.game.actor is not self:
            raise GameFrameValueError('The actor is not in turn')
