from abc import ABC
from collections.abc import Mapping, Sequence
from typing import Any, Optional, TypeVar, Union, final

from gameframe.game import Action, Actor, Environment, Game
from gameframe.sequential.exceptions import ActorOutOfTurnException
from gameframe.utils import override

__all__ = ['SequentialGame', 'SequentialAction']

SG = TypeVar('SG', bound='SequentialGame')
E = TypeVar('E', bound=Environment)
N = TypeVar('N', bound=Actor)
P = TypeVar('P', bound=Actor)


class SequentialGame(Game[SG, E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time.

    The actor in turn can be accessed through the actor property of the SequentialGame instance. The subclasses should
    define the actor who is the first to act. If a sequential game is terminal, its protected actor attribute must be
    set to None to denote such.
    """

    def __init__(self: SG, environment: E, nature: N, players: Sequence[P], initial_actor_index: Optional[int]) -> None:
        super().__init__(environment, nature, players)

        self._actor: Optional[Union[N, P]] = self.nature if initial_actor_index is None else self.players[
            initial_actor_index]

    @property
    @final
    def actor(self: SG) -> Optional[Union[N, P]]:
        """
        :return: the actor in turn to act of the sequential game
        """
        return self._actor

    @property
    @final
    @override
    def terminal(self: SG) -> bool:
        return self.actor is None

    @property
    @override
    def _information(self: SG) -> Mapping[str, Any]:
        return {
            **super()._information,
            'actor': self.actor,
        }


class SequentialAction(Action[SG, E, N, P], ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    @override
    def _verify(self) -> None:
        super()._verify()

        if self.actor is not self.game.actor:
            raise ActorOutOfTurnException()
