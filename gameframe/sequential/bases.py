from abc import ABC, abstractmethod
from typing import Any, Optional, TypeVar, Union

from gameframe.game import Action, E, Game, N, P

SG = TypeVar('SG', bound='SequentialGame')


class SequentialGame(Game[SG, E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time.

    The actor in turn can be accessed through the actor property of the SequentialGame instance. The initial_actor
    abstract property should be overridden by the subclasses to represent the actor who is the first to act. If a
    sequential game is terminal, its protected actor attribute must be set to None to denote such.
    """

    def __init__(self) -> None:
        super().__init__()

        self._actor: Optional[Union[N, P]] = self._initial_actor

    @property
    def actor(self) -> Optional[Union[N, P]]:
        """
        :return: the actor in turn to act of the sequential game
        """
        return self._actor

    @property
    def terminal(self) -> bool:
        return self.actor is None

    @property
    def _information(self) -> dict[str, Any]:
        return {
            **super()._information,
            'actor': self.actor,
        }

    @property
    @abstractmethod
    def _initial_actor(self) -> Optional[Union[N, P]]:
        pass


class SequentialAction(Action[SG, E, N, P], ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    def _verify(self) -> None:
        super()._verify()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not an instance of SequentialGame')
        if self.actor is not self.game.actor:
            raise ValueError('The actor is not in turn to act')
