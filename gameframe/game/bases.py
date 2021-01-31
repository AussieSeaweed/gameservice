from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence


class BaseGame(ABC):
    """BaseGame is the abstract base class for all games.

    Every game has the following elements that need to be defined: the environment, the nature, and the players.
    """

    @property
    @abstractmethod
    def env(self) -> BaseEnv:
        """
        :return: the environment of this game
        """
        pass

    @property
    @abstractmethod
    def nature(self) -> BaseActor:
        """
        :return: the nature of this game
        """
        pass

    @property
    @abstractmethod
    def players(self) -> Sequence[BaseActor]:
        """
        :return: the players of this game
        """
        pass

    @property
    @abstractmethod
    def is_terminal(self) -> bool:
        """
        :return: True if this game is terminal, else False
        """
        pass


class BaseEnv(ABC):
    """BaseEnv is the abstract base class for all environments.

    The environment contains global information about a game state that does not belong to any actor in particular and
    is public.
    """

    def __repr__(self) -> str:
        return 'Env'

    @property
    @abstractmethod
    def game(self) -> BaseGame:
        """
        :return: the game of this environment
        """
        pass


class BaseActor(ABC):
    """BaseActor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold private
    information regarding a game state that no other player knows about.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    def __repr__(self) -> str:
        try:
            return f'Player {self.index}'
        except ValueError:
            return 'Nature'

    @property
    def index(self) -> int:
        try:
            return self.game.players.index(self)
        except ValueError:
            raise ValueError('The nature does not have an associated index')

    @property
    @abstractmethod
    def game(self) -> BaseGame:
        """
        :return: the game of this actor
        """
        pass

    @property
    @abstractmethod
    def actions(self) -> Sequence[BaseAction]:
        """
        :return: the actions of this actor
        """
        pass


class BaseAction(ABC):
    """BaseAction is the abstract base class for all actions."""

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    @abstractmethod
    def game(self) -> BaseGame:
        """
        :return: the game of this action
        """
        pass

    @property
    @abstractmethod
    def actor(self) -> BaseActor:
        """
        :return: the actor of this action
        """
        pass

    @property
    @abstractmethod
    def is_applicable(self) -> bool:
        """
        :return: True if this action can be applied else False
        """
        pass

    @abstractmethod
    def act(self) -> None:
        """Applies this action to the game.

        The overridden act method should first call the super method and then make the changes in the game.

        :return: None
        :raise ActionException: if this action cannot be applied
        """
        pass
