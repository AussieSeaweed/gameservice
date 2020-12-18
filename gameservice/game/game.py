"""
This module defines a general game structure in gameservice.
"""
from abc import ABC, abstractmethod


class Game(ABC):
    """
    This is a base class for all games in gameservice.
    """

    def __init__(self):
        """
        Constructs the Game instance. Initializes the environment, nature, players, and logs.
        """
        self.__environment = self._create_environment()
        self.__nature = self._create_nature()
        self.__players = self._create_players()

        self.__logs = []

    @abstractmethod
    def _create_environment(self):
        """
        Creates the environment of the game.
        :return: the environment of the game
        """
        pass

    @abstractmethod
    def _create_nature(self):
        """
        Creates the nature of the game.
        :return: the nature of the game
        """
        pass

    @abstractmethod
    def _create_players(self):
        """
        Creates the players of the game.
        :return: a list of the players of the game
        """
        pass

    @property
    def environment(self):
        """
        Returns the environment of the game.
        :return: the environment of the game
        """
        return self.__environment

    @property
    def nature(self):
        """
        Returns the nature of the game.
        :return: the nature of the game
        """
        return self.__nature

    @property
    def players(self):
        """
        Returns the players of the game.
        :return: a list of the players of the game
        """
        return self.__players

    @property
    def logs(self):
        """
        Returns the logs of the game.
        :return: a list of the logs of the game
        """
        return self.__logs

    @property
    @abstractmethod
    def terminal(self):
        """
        Returns the terminality of the game.
        :return: a boolean value of the terminality of the game
        """
        pass


class SeqGame(Game, ABC):
    """
    This is a base class for all sequential games in gameservice. When the game is terminal, the player member variable
    must be set to None.
    """

    def __init__(self):
        """
        Constructs the SeqGame instance. Initializes the player.
        """
        super().__init__()

        self.player = self._initial_player

    @property
    @abstractmethod
    def _initial_player(self):
        """
        Returns the initial player of the game.
        :return: the initial player of the game
        """
        pass

    @property
    def terminal(self):
        """
        Returns whether or not the player member variable is None which corresponds to the terminality of the game.
        :return: a boolean value of whether or not the player member variable is None
        """
        return self.player is None
