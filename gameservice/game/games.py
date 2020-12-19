"""
This module defines games and sequential games in gameservice.
"""
from abc import ABC, abstractmethod


class Game(ABC):
    """
    This is a class that represents games.
    """

    def __init__(self):
        """
        Constructs a Game instance. Initializes the environment, nature, players, and logs of the game.
        """
        self.__environment = self._create_environment()
        self.__nature = self._create_nature()
        self.__players = self._create_players()

        self.__logs = []

    @abstractmethod
    def _create_environment(self):
        """
        Creates an environment.

        :return: an environment
        """
        pass

    @abstractmethod
    def _create_nature(self):
        """
        Creates a nature.

        :return: a nature
        """
        pass

    @abstractmethod
    def _create_players(self):
        """
        Creates players.

        :return: a list of players
        """
        pass

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

    @property
    @abstractmethod
    def terminal(self):
        """
        :return: a boolean value of the terminality of the game
        """
        pass


class SeqGame(Game, ABC):
    """
    This is a class that represents sequential games. If a sequential game is terminal, its player member variable must
    be set to None.
    """

    def __init__(self):
        """
        Constructs a SeqGame instance. Initializes the player.
        """
        super().__init__()

        self.player = self._initial_player

    @property
    @abstractmethod
    def _initial_player(self):
        """
        :return: the initial player of the game
        """
        pass

    @property
    def terminal(self):
        """
        Returns the terminality of the game. Sequential games are terminal if the player member variable is None.

        :return: a boolean value of the terminality of the game
        """
        return self.player is None
