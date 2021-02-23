from abc import ABC, abstractmethod
from collections import Sequence
from typing import Generic, Optional, TypeVar, Union, final

from gameframe.game import ActionException, BaseActor
from gameframe.game._generics import A, Action, Game, N, P
from gameframe.sequential.bases import BaseSeqGame

SG = TypeVar('SG', bound=BaseSeqGame)


class SeqGame(Game[N, P], BaseSeqGame, Generic[N, P], ABC):
    def __init__(self, nature: N, players: Sequence[P], actor: Optional[Union[N, P]]):
        super().__init__(nature, players)

        self._actor: Optional[Union[N, P]] = actor

    @property
    @final
    def actor(self) -> Optional[Union[N, P]]:
        return self._actor


class SeqAction(Action[SG, A], ABC):
    @property
    @abstractmethod
    def next_actor(self) -> Optional[BaseActor]:
        pass

    def act(self) -> None:
        super().act()

        self.game._actor = self.next_actor

    def verify(self) -> None:
        super().verify()

        if self.game.actor is not self.actor:
            raise ActionException('The actor is not in turn')
