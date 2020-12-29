from abc import ABC, abstractmethod


class Game(ABC):
    """Game is the abstract base class for all games.

    It provides a rigid definition on which various games can be defined. Every game has the following elements that
    need to be defined:

        - The game
        - The environment
        - The nature
        - The players

    The game class is a wrapper class that envelops all the elements of the game: the environment, the nature, and
    the players. They each represent elements of the game.

    The environment contains global information about a game state that does not belong to any player in particular and
    is public.

    The nature is a player that represents the environment and carries out chance actions. The nature may hold
    private information regarding a game state that no other player knows about. However, the nature should not be
    aware of any private information held by other players in the game.

    The players of the game are the entities that act non-chance actions. A player is aware of the environment
    information, all the public player information of other players, and the private player information of itself.
    """

    def __init__(self):
        self.__environment = self._create_environment()
        self.__nature = self._create_nature()
        self.__players = self._create_players()

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
        :return: the players of the game
        """
        return self.__players

    @property
    @abstractmethod
    def terminal(self):
        """
        :return: True if the game is terminal, False otherwise
        """
        pass

    @property
    def _information(self):
        return {}

    @abstractmethod
    def _create_environment(self):
        pass

    @abstractmethod
    def _create_nature(self):
        pass

    @abstractmethod
    def _create_players(self) :
        pass
