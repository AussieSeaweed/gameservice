from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Union

from gameframe.game import Action, E, Game, N, P

SG = TypeVar('SG', bound='SequentialGame')


class SequentialGame(Game[SG, E, N, P], Generic[SG, E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one player can act at a time.

    The player in turn can be accessed through the player attribute of the SequentialGame instance. The initial_player
    abstract property should be overridden by the subclasses to represent the player who is the first to act. If a
    sequential game is terminal, its player attribute must be set to None to denote such.
    """

    def __init__(self: SG) -> None:
        super().__init__()

        self._actor: Union[N, P] = self._initial_actor

    @property
    def actor(self: SG) -> Union[N, P]:
        """
        :return: the actor in turn to act of the sequential game
        """
        return self._actor

    @property
    def terminal(self: SG) -> bool:
        return self.actor is None

    @property
    def _information(self: SG) -> dict[str, Any]:
        return {
            **super()._information,
            'actor': self.actor,
        }

    @property
    @abstractmethod
    def _initial_actor(self: SG) -> Union[N, P]:
        pass


class SequentialAction(Action[SG, E, N, P], Generic[SG, E, N, P], ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    def _verify(self: SequentialAction[SG, E, N, P]) -> None:
        super()._verify()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not an instance of SequentialGame')
        if self.actor is not self.game.actor:
            raise ValueError('The acting player is not in turn to act')
