from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterator, Sequence, TypeVar, Union

from gameframe.game.bases import BaseAction, BaseActor, BaseEnv
from gameframe.game.exceptions import ActionException

E = TypeVar('E', bound=BaseEnv, covariant=True)
N = TypeVar('N', bound=BaseActor, covariant=True)
P = TypeVar('P', bound=BaseActor, covariant=True)
A = TypeVar('A', bound=BaseActor, covariant=True)


class Game(Generic[E, N, P], ABC):
    """Game is the generic abstract base class for all games.

    Every game has the following elements that need to be defined: the environment, the nature, and the players.
    """

    def __init__(self, env: E, nature: N, players: Sequence[P]):
        self.__env = env
        self.__nature = nature
        self.__players = tuple(players)

    @property
    def env(self) -> E:
        """
        :return: the environment of this game
        """
        return self.__env

    @property
    def nature(self) -> N:
        """
        :return: the nature of this game
        """
        return self.__nature

    @property
    def players(self) -> Sequence[P]:
        """
        :return: the players of this game
        """
        return self.__players

    @property
    @abstractmethod
    def is_terminal(self) -> bool:
        """
        :return: True if this game is terminal, else False
        """
        pass


class Env(BaseEnv, Generic[E, N, P], ABC):
    """Env is the generic abstract base class for all environments."""

    def __init__(self, game: Game[E, N, P]):
        self._game = game


class Actor(BaseActor, Iterator[Union[N, P]], Generic[E, N, P], ABC):
    """Actor is the generic abstract base class for all actors."""

    def __init__(self, game: Game[E, N, P]):
        self._game = game

    def __next__(self) -> Union[N, P]:
        if self is self._game.nature:
            return self._game.nature
        else:
            return self._game.players[(self._game.players.index(self) + 1) % len(self._game.players)]


class Action(BaseAction, Generic[E, N, P, A], ABC):
    """Action is the generic abstract base class for all actions."""

    def __init__(self, game: Game[E, N, P], actor: A):
        self._game = game
        self._actor = actor

    @property
    def is_applicable(self) -> bool:
        return not self._game.is_terminal and (self._actor is self._game.nature or self._actor in self._game.players)

    def act(self) -> None:
        if not self.is_applicable:
            raise ActionException()
