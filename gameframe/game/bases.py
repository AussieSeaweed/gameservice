from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence


class BaseGame(ABC):
    """BaseGame is the abstract base class for all games.

    Every game has to define its nature, and players.
    """

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


class BaseActor(ABC):
    """BaseActor is the abstract base class for all actors.

    The nature and the player are the types of actors in the game.

    The nature is an actor that represents the environment and carries out chance actions. The nature may hold private
    information regarding a game state that no other player knows about.

    The players of the game are the actors that act non-chance actions. A player is aware of the environment
    information, all the public information of other actors, and the private information of itself.
    """

    @property
    @abstractmethod
    def game(self) -> BaseGame:
        """
        :return: the game of this actor
        """
        pass
