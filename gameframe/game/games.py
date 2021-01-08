from abc import ABC, abstractmethod
from typing import final


class Game(ABC):
    """Game is the abstract base class for all games.

    Every game has the following elements that need to be defined: the environment, the nature actor, and the player
    actors.
    """

    def __init__(self, environment, nature, players):
        self.__environment = environment
        self.__nature = nature
        self.__players = players

    @property
    @final
    def environment(self):
        """
        :return: the environment of this game
        """
        return self.__environment

    @property
    @final
    def nature(self):
        """
        :return: the nature of this game
        """
        return self.__nature

    @property
    @final
    def players(self):
        """
        :return: the players of this game
        """
        return self.__players

    @property
    @abstractmethod
    def terminal(self):
        """
        :return: True if this game is terminal, False otherwise
        """
        pass

    @property
    def _information(self):
        return {}
