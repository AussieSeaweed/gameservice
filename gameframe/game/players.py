"""
This module defines players and natures in gameframe.
"""
from abc import ABC, abstractmethod
from typing import Generic
from .utils import G, E, N, P


class Player(Generic[G, E, N, P], ABC):
    """
    This is a class that represents players.
    """

    def __init__(self, game: G, index: int):
        self.__game: G = game
        self.__index: int = index

    @property
    def game(self) -> G:
        """
        :return: the game of the player
        """
        return self.__game

    @property
    def index(self) -> int:
        """
        :return: the index of the player
        """
        return self.__index

    @property
    @abstractmethod
    def payoff(self):
        """
        :return: the payoff of the player
        """
        pass

    @property
    @abstractmethod
    def actions(self):
        """
        :return: a list of actions of the player
        """
        pass

    @property
    @abstractmethod
    def info_set(self):
        """
        :return: the info-set of the player
        """
        pass

    @property
    def nature(self):
        """
        :return: a boolean value of whether or not the player is the nature
        """
        return self is self.game.nature

    def __next__(self):
        """
        Finds the next player of the game unless the player is the nature, in which case the nature is returned.

        :return: the next player or the nature of the game
        """
        return self.game.nature if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        """
        Converts the player into a string representation.

        :return: the string representation of the player
        """
        return f'Player {self.index}'
