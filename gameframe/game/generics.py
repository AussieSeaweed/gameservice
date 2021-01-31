from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from gameframe.game.bases import BaseAction, BaseActor, BaseEnv, BaseGame
from gameframe.game.exceptions import ActionException

G = TypeVar('G', bound=BaseGame, covariant=True)
E = TypeVar('E', bound=BaseEnv, covariant=True)
N = TypeVar('N', bound=BaseActor, covariant=True)
P = TypeVar('P', bound=BaseActor, covariant=True)
A = TypeVar('A', bound=BaseActor, covariant=True)


class Game(Generic[E, N, P], ABC):
    """Game is the generic abstract base class for all games."""

    def __init__(self, env: E, nature: N, players: Sequence[P]):
        self.__env = env
        self.__nature = nature
        self.__players = tuple(players)

    @property
    def env(self) -> E:
        return self.__env

    @property
    def nature(self) -> N:
        return self.__nature

    @property
    def players(self) -> Sequence[P]:
        return self.__players


class Env(BaseEnv, Generic[G], ABC):
    """Env is the generic abstract base class for all environments."""

    def __init__(self, game: G):
        self.__game = game

    @property
    def game(self) -> G:
        return self.__game


class Actor(BaseActor, Generic[G], ABC):
    """Actor is the generic abstract base class for all actors."""

    def __init__(self, game: G):
        self.__game = game

    @property
    def game(self) -> G:
        return self.__game

    @property
    @abstractmethod
    def actions(self: A) -> Sequence[Action[G, A]]:
        pass


class Action(BaseAction, Generic[G, A], ABC):
    """Action is the generic abstract base class for all actions."""

    def __init__(self, game: G, actor: A):
        self.__game = game
        self.__actor = actor

    @property
    def game(self) -> G:
        return self.__game

    @property
    def actor(self) -> A:
        return self.__actor

    @property
    def is_applicable(self) -> bool:
        return not self.game.is_terminal and (self.actor is self.game.nature or self.actor in self.game.players)

    def act(self) -> None:
        if not self.is_applicable:
            raise ActionException()
