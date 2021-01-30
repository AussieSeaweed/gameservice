from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar, Union

from gameframe.game.exceptions import ActionException


class Env(ABC):
    """Env is the base class for all environments.

    The environment contains global information about a game state that does not belong to any actor in particular and
    is public.
    """
    pass


class Actor(ABC):
    """Actor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold private
    information regarding a game state that no other player knows about.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    @property
    @abstractmethod
    def actions(self: A) -> Sequence[Action[Env, Actor, Actor, A]]:
        """
        :return: the actions of this actor
        """
        pass


E = TypeVar('E', bound=Env, covariant=True)
N = TypeVar('N', bound=Actor, covariant=True)
P = TypeVar('P', bound=Actor, covariant=True)
A = TypeVar('A', bound=Actor, covariant=True)


class Game(Generic[E, N, P], ABC):
    """Game is the abstract base class for all games.

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


class Action(Generic[E, N, P, A], ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, game: Game[E, N, P], actor: A):
        self._game = game
        self._actor = actor

    @property
    def is_applicable(self) -> bool:
        """
        :return: True if this action can be applied else False
        """
        return not self._game.is_terminal and (self._actor is self._game.nature or self._actor in self._game.players)

    def act(self) -> None:
        """Applies this action to the game.

        The overridden act method should first call the super method and then make the changes in the game.

        :return: None
        :raise ActionException: if this action cannot be applied
        """
        if not self.is_applicable:
            raise ActionException()

    def next_actor(self, actor: Actor) -> Union[N, P]:
        """Gets the next player in the game.

        :param actor: the actor from which the next actor is obtained
        :return: the next player of the supplied player
        """
        if actor is self._game.nature:
            return self._game.nature
        else:
            return self._game.players[(self._game.players.index(actor) + 1) % len(self._game.players)]
