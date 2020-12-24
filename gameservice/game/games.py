"""
This module defines games and sequential games in gameservice.
"""
from abc import ABC, abstractmethod


class Game(ABC):
    """
    This is a class that represents games.
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
    This is a class that represents sequential games. In sequential games, only one player can act at a time. The player
    in turn is stored in the player attribute of the SequentialGame instance. If a sequential game is terminal, its
    player attribute variable must be set to None.
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
