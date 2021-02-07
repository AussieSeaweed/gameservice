from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from gameframe.game.bases import BaseActor, BaseGame
from gameframe.game.exceptions import ActionException

G = TypeVar('G', bound=BaseGame, covariant=True)
N = TypeVar('N', bound=BaseActor, covariant=True)
P = TypeVar('P', bound=BaseActor, covariant=True)
A = TypeVar('A', bound=BaseActor, covariant=True)


class Game(BaseGame, Generic[N, P], ABC):
    def __init__(self, nature: N, players: Sequence[P]):
        self.__nature = nature
        self.__players = tuple(players)

    @property
    def nature(self) -> N:
        return self.__nature

    @property
    def players(self) -> Sequence[P]:
        return self.__players


class Actor(BaseActor, Generic[G], ABC):
    def __init__(self, game: G):
        self.__game = game

    @property
    def game(self) -> G:
        return self.__game


class Action(Generic[G, A], ABC):
    def __init__(self, game: G, actor: A):
        self.game = game
        self.actor = actor

    def act(self) -> None:
        self.verify()
        self.apply()

    def verify(self) -> None:
        if self.game.terminal:
            raise ActionException('The action is applied to a terminal game')

    @abstractmethod
    def apply(self) -> None:
        pass
