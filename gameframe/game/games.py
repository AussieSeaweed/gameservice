from abc import ABC, abstractmethod


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
    def environment(self):
        """
        :return: the environment of this game
        """
        return self.__environment

    @property
    def nature(self):
        """
        :return: the nature of this game
        """
        return self.__nature

    @property
    def players(self):
        """
        :return: the players of this game
        """
        return self.__players

    @property
    def information(self):
        """
        :return: the information of this game
        """
        return {}

    @property
    @abstractmethod
    def is_terminal(self):
        """
        :return: True if this game is terminal, False otherwise
        """
        pass
