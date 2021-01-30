from __future__ import annotations

from abc import ABC
from typing import Generic, Optional, TypeVar, Union

from gameframe.game.bases import A
from gameframe.game.generics import Action, Env, Game, N, P
from gameframe.sequential.bases import BaseSeqEnv, BaseSeqGame

G = TypeVar('G', bound=BaseSeqGame, covariant=True)
E = TypeVar('E', bound=BaseSeqEnv, covariant=True)


class SeqGame(Game[E, N, P], BaseSeqGame, ABC):
    """SeqGame is the generic abstract base class for all sequential games."""
    pass


class SeqEnv(Env[G], BaseSeqEnv, Generic[G, N, P], ABC):
    """SeqEnv is the generic abstract base class for all sequential environments."""

    def __init__(self, game: G, actor: Optional[Union[N, P]]):
        super().__init__(game)

        self._actor = actor

    @property
    def actor(self) -> Optional[Union[N, P]]:
        return self._actor


class SeqAction(Action[G, A], ABC):
    """SeqAction is the generic abstract base class for all sequential actions."""

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self._game.env.actor is self._actor
