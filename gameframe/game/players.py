from abc import ABC, abstractmethod
from typing import Generic, List, Optional

from .actions import Action
from .infosets import InfoSet
from .utils import E, G, N, P


class Player(Generic[G, E, N, P], ABC):
    """Player is the abstract base class for all players."""

    def __init__(self, game: G):
        self.__game: G = game

    @property
    def game(self) -> G:
        """
        :return: the game of the player
        """
        return self.__game

    @property
    def index(self) -> Optional[int]:
        """
        :return: the index of the player
        """
        return None if self.nature else self.game.players.index(self)

    @property
    def nature(self) -> bool:
        """
        :return: True if the player is nature, False otherwise
        """
        return self is self.game.nature

    def __next__(self) -> Optional[P]:
        return None if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self) -> str:
        return 'Nature' if self.nature else f'Player {self.index}'

    @property
    @abstractmethod
    def actions(self) -> List[Action[G, E, N, P]]:
        """
        :return: the actions of the player
        """
        pass

    @property
    @abstractmethod
    def info_set(self) -> InfoSet[G, E, N, P]:
        """
        :return: the info-set of the player
        """
        pass

    @property
    @abstractmethod
    def payoff(self) -> int:
        """
        :return: the payoff of the player
        """
        pass
