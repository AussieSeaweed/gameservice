from abc import ABC, abstractmethod
from typing import Generic, List

from .utils import E, G, Log, N, P


class Game(Generic[G, E, N, P], ABC):
    """Game is the abstract base class for all games.
    It provides a rigid definition on which various games can be defined. Every game has the following elements that
    need to be defined:

    * The game
    * The environment
    * Nature
    * The players

    The game class is a wrapper class that envelops all the elements of the game: the environment, nature, and the
    players. They each represent elements of the game.

    The environment contains global information about a game state. This information should not belong to any player in
    particular and should be all public.

    Nature is a player that represents the environment and carries out chance actions. Nature may hold private
    information regarding a game state that no other player knows about. However, nature should not be aware of
    private information held by other players in the game.

    The players of the game are the entities that act non-chance actions. A player is aware of all public player
    information of other players and private player information of itself.
    """

    def __init__(self):
        self.__environment: E = self.create_environment()
        self.__nature: N = self.create_nature()
        self.__players: List[P] = self.create_players()

        self.__logs: List[Log] = []

    @property
    def environment(self) -> E:
        """
        :return: the game environment
        """
        return self.__environment

    @property
    def nature(self) -> N:
        """
        :return: the game nature
        """
        return self.__nature

    @property
    def players(self) -> List[P]:
        """
        :return: the game players
        """
        return self.__players

    @property
    def logs(self) -> List[Log]:
        """
        :return: the game logs
        """
        return self.__logs

    @abstractmethod
    def create_environment(self) -> E:
        """Creates the game environment.

        :return: the created environment
        """
        pass

    @abstractmethod
    def create_nature(self) -> N:
        """Creates the game nature.

        :return: the created nature
        """
        pass

    @abstractmethod
    def create_players(self) -> List[P]:
        """Creates the game players.

        :return: the created players
        """
        pass

    @property
    @abstractmethod
    def terminal(self) -> bool:
        """Determines whether or not the game is terminal.

        :return: True if the game is terminal; False otherwise
        """
        pass
