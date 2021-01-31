from abc import ABC
from typing import Generic, Optional, TypeVar, Union

from gameframe.game.generics import A, Action, Env, Game, N, P
from gameframe.sequential.bases import BaseSeqEnv, BaseSeqGame

G = TypeVar('G', bound=BaseSeqGame, covariant=True)
E = TypeVar('E', bound=BaseSeqEnv, covariant=True)


class SeqGame(Game[E, N, P], BaseSeqGame, ABC):
    pass


class SeqEnv(Env[G], BaseSeqEnv, Generic[G, N, P], ABC):
    def __init__(self, game: G, actor: Optional[Union[N, P]]):
        super().__init__(game)

        self._actor = actor

    @property
    def actor(self) -> Optional[Union[N, P]]:
        return self._actor


class SeqAction(Action[G, A], ABC):
    def verify(self) -> None:
        super().verify()

        if self.game.env.actor is not self.actor:
            raise ValueError('Actor not in turn')
