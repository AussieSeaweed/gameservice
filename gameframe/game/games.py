"""
This module defines games and sequential games in gameframe.
"""
from abc import ABC, abstractmethod


class Game(ABC):
    """
    This is a class that represents games.

    Implementations of different games should inherit this class from which they can be instantiated. When a Game
    instance is created, its environment, nature, and players are also created through the invocations of
    corresponding create methods, which should be overridden by the subclasses. Also, every subclass should override the
    terminal property accordingly.
    """

    def __init__(self):
        self.__environment = self.create_environment()
        self.__nature = self.create_nature()
        self.__players = self.create_player()

        self.__logs = []

    @property
    def environment(self):
        """
        :return: the environment of the game
        """
        return self.__environment

    @property
    def nature(self):
        """
        :return: the nature of the game
        """
        return self.__nature

    @property
    def players(self):
        """
        :return: a list of the players of the game
        """
        return self.__players

    @property
    def logs(self):
        """
        :return: a list of the logs of the game
        """
        return self.__logs

    @abstractmethod
    def create_environment(self):
        """
        Creates an environment.

        :return: an environment
        """
        pass

    @abstractmethod
    def create_nature(self):
        """
        Creates a nature.

        :return: a nature
        """
        pass

    @abstractmethod
    def create_player(self):
        """
        Creates players.

        :return: a list of players
        """
        pass

    @property
    @abstractmethod
    def terminal(self):
        """
        :return: a boolean value of the terminality of the game
        """
        pass


class SequentialGame(Game, ABC):
    """
    This is a class that represents sequential games.

    In sequential games, only one player can act at a time. The player in turn can be accessed through the player
    attribute of the SequentialGame instance. The initial_player abstract property should be overridden by the
    subclasses to represent the player who is the first to act. If a sequential game is terminal, its player attribute
    must be set to None to denote such.
    """

    def __init__(self):
        super().__init__()

        self.player = self.initial_player

    @property
    def terminal(self):
        return self.player is None

    @property
    @abstractmethod
    def initial_player(self):
        """
        :return: the initial player of the sequential game
        """
        pass
