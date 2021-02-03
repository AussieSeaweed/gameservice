from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, Union

from gameframe.game import ActionException, BaseActor
from gameframe.game.generics import A, Action, Env, Game, N, P
from gameframe.sequential.bases import BaseSeqEnv, BaseSeqGame

G = TypeVar('G', bound=BaseSeqGame, covariant=True)
E = TypeVar('E', bound=BaseSeqEnv, covariant=True)


class SeqGame(Game[E, N, P], BaseSeqGame, ABC):
    pass


class SeqEnv(Env[G], BaseSeqEnv, Generic[G, N, P], ABC):
    def __init__(self, game: G, actor: Optional[Union[N, P]]):
        super().__init__(game)

        self._actor: Optional[Union[N, P]] = actor

    @property
    def actor(self) -> Optional[Union[N, P]]:
        return self._actor


class SeqAction(Action[G, A], ABC):
    @property
    @abstractmethod
    def next_actor(self) -> Optional[BaseActor]:
        pass

    def apply(self) -> None:
        super().apply()

        self.game.env._actor = self.next_actor

    def verify(self) -> None:
        super().verify()

        if self.game.env.actor is not self.actor:
            raise ActionException('Actor not in turn')
