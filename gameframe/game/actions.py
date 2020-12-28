from abc import ABC, abstractmethod
from typing import Generic

from .utils import E, G, N, P


class Action(Generic[G, E, N, P], ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, player: P):
        self.__player: P = player

    def act(self) -> None:
        """Applies the action to the game of the action.

        The overridden act method should first call the super method and then make the necessary modifications to the
        game.

        :return: None
        :raise ValueError: if the action integrity verification fails
        """
        self._verify()

    @property
    def game(self) -> G:
        """
        :return: the game of the action
        """
        return self.player.game

    @property
    def player(self) -> P:
        """
        :return: the player of the action
        """
        return self.__player

    @property
    @abstractmethod
    def chance(self) -> bool:
        """
        :return: True if the action is a chance action, False otherwise
        """
        pass

    @property
    @abstractmethod
    def public(self) -> bool:
        """
        :return: True if the action is a public action, False otherwise
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def _verify(self) -> None:
        if self.game.terminal:
            raise ValueError('Actions are not applicable to terminal games')
        elif self.chance != self.player.nature:
            raise ValueError('Nature acts chance actions')
