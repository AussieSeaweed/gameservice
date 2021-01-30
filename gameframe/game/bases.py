from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Sequence


class BaseEnv(ABC):
    """BaseEnv is the abstract base class for all environments.

    The environment contains global information about a game state that does not belong to any actor in particular and
    is public.
    """
    pass


class BaseActor(Iterator['BaseActor'], ABC):
    """BaseActor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold private
    information regarding a game state that no other player knows about.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    @abstractmethod
    def __next__(self) -> BaseActor:
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

    @property
    @abstractmethod
    def is_applicable(self) -> bool:
        """
        :return: True if this action can be applied else False
        """
        pass

    def act(self) -> None:
        """Applies this action to the game.

        The overridden act method should first call the super method and then make the changes in the game.

        :return: None
        :raise ActionException: if this action cannot be applied
        """
        pass
