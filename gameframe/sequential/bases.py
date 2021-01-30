from abc import ABC
from typing import Optional, TypeVar

from gameframe.game.bases import A, Action, Actor, Env, Game, N, P


class SeqEnv(Env, ABC):
    """SeqEnv is the abstract base class for all sequential environments."""

    def __init__(self, actor: Optional[Actor]):
        self._actor = actor

    @property
    def actor(self) -> Optional[Actor]:
        """
        :return: the actor of the sequential game of this environment
        """
        return self._actor


E = TypeVar('E', bound=SeqEnv, covariant=True)


class SeqGame(Game[E, N, P], ABC):
    """SeqGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    @property
    def is_terminal(self) -> bool:
        return self.env.actor is None


class SeqAction(Action[E, N, P, A], ABC):
    """SeqAction is the abstract base class for all sequential actions."""

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self._game.env.actor is self._actor
