"""
This module defines a general game structure.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from . import Environment, Log, Nature, Player


class Game(ABC):
    """
    This is a base class for all games in gameservice.
    """

    def __init__(self: Game) -> None:
        """
        Constructs the Game instance. Initializes the environment, nature, players, and logs.
        """
        self.__environment: Optional[Environment] = self._create_environment()
        self.__nature: Optional[Nature] = self._create_nature()
        self.__players: Optional[List[Player]] = self._create_players()

        self.__logs: List[Log] = []

    @abstractmethod
    def _create_environment(self: Game) -> Optional[Environment]:
        """
        Creates the environment of the game.
        :return: The environment of the game
        """
        pass

    @abstractmethod
    def _create_nature(self: Game) -> Optional[Nature]:
        """
        Creates the nature of the game.
        :return: The nature of the game
        """
        pass

    @abstractmethod
    def _create_players(self: Game) -> Optional[List[Player]]:
        """
        Creates the players of the game.
        :return: A list of the players of the game
        """
        pass

    @property
    def environment(self: Game) -> Optional[Environment]:
        """
        Returns the environment of the game.
        :return: The environment of the game
        """
        return self.__environment

    @property
    def nature(self: Game) -> Optional[Nature]:
        """
        Returns the nature of the game.
        :return: The nature of the game
        """
        return self.__nature

    @property
    def players(self: Game) -> Optional[List[Player]]:
        """
        Returns the players of the game.
        :return: A list of the players of the game
        """
        return self.__players

    @property
    def logs(self: Game) -> List[Log]:
        """
        Returns the logs of the game.
        :return: A list of the logs of the game
        """
        return self.__logs

    @property
    @abstractmethod
    def terminal(self: Game) -> bool:
        """
        Returns the terminality of the game.
        :return: A boolean value of the terminality of the game
        """
        pass


class SeqGame(Game, ABC):
    """
    This is a base class for all sequential games in gameservice.
    """

    def __init__(self: SeqGame) -> None:
        """
        Constructs the SeqGame instance. Initializes the player member variable that corresponds to the player to act.
        When the game is terminal, the player must be set to None.
        """
        super().__init__()

        self.player: Optional[Player] = self._initial_player

    @property
    @abstractmethod
    def _initial_player(self: SeqGame) -> Optional[Player]:
        """
        Returns the initial player of the game.
        :return: The initial player of the game
        """
        pass

    @property
    def terminal(self: SeqGame) -> bool:
        """
        Returns whether or not the player member variable is None which corresponds to the terminality of the game.
        :return: A boolean value of whether or not the player member variable is None
        """
        return self.player is None
