from abc import ABC
from typing import Optional, TypeVar, Union

from gameframe.game.generics import A, Action, Env, Game, N, P
from gameframe.sequential.bases import BaseSeqEnv

E = TypeVar('E', bound=BaseSeqEnv, covariant=True)


class SeqGame(Game[E, N, P], ABC):
    """SeqGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    @property
    def is_terminal(self) -> bool:
        return self.env.actor is None


class SeqEnv(BaseSeqEnv, Env[E, N, P], ABC):
    """SeqEnv is the abstract base class for all sequential environments."""

    def __init__(self, game: SeqGame[E, N, P], actor: Optional[Union[N, P]]):
        super().__init__(game)

        self._actor = actor

    @property
    def actor(self) -> Optional[Union[N, P]]:
        return self._actor


class SeqAction(Action[E, N, P, A], ABC):
    """SeqAction is the abstract base class for all sequential actions."""

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self._game.env.actor is self._actor
