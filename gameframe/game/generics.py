from abc import ABC, abstractmethod
from typing import Generic, MutableSequence, Sequence, TypeVar

from gameframe.game.bases import BaseActor, BaseEnv, BaseGame
from gameframe.game.exceptions import ActionException

G = TypeVar('G', bound=BaseGame, covariant=True)
E = TypeVar('E', bound=BaseEnv, covariant=True)
N = TypeVar('N', bound=BaseActor, covariant=True)
P = TypeVar('P', bound=BaseActor, covariant=True)
A = TypeVar('A', bound=BaseActor, covariant=True)


class Game(BaseGame, Generic[E, N, P], ABC):
    def __init__(self, env: E, nature: N, players: Sequence[P]):
        self._env: E = env
        self._nature: N = nature
        self._players: MutableSequence[P] = list(players)

    @property
    def env(self) -> E:
        return self._env

    @property
    def nature(self) -> N:
        return self._nature

    @property
    def players(self) -> Sequence[P]:
        return tuple(self._players)


class Env(BaseEnv, Generic[G], ABC):
    def __init__(self, game: G):
        self.__game = game

    @property
    def game(self) -> G:
        return self.__game


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

    def apply(self) -> None:
        self.verify()
        self.act()

    def verify(self) -> None:
        if self.game.is_terminal:
            raise ActionException('The action is applied to a terminal game')

    @abstractmethod
    def act(self) -> None:
        pass
