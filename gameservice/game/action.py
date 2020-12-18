"""
This module defines a general game action in gameservice.
"""
from abc import ABC, abstractmethod

from .exception import GamePlayerException, GameTerminalException, GameTypeException
from .game import SeqGame
from .utils import Log


class Action(ABC):
    """
    This is a base class for all actions in gameservice.
    """

    def __init__(self, player):
        """
        Constructs the Action instance. Stores the player taking the action.
        :param player: the player who takes the action
        """
        self.__player = player

    @property
    def player(self):
        """
        Returns the player who takes the action.
        :return: the player who takes the action
        """
        return self.__player

    @property
    def game(self):
        """
        Returns the game which the action modifies.
        :return: the game which the action modifies
        """
        return self.player.game

    def _validate(self):
        """
        Validates the integrity of the action.
        :return: None
        :raise GameTerminalException: if the game is terminal
        :raise GamePlayerException: if the action is a chance action but the player is not nature or vice versa
        """

        if self.game.terminal:
            raise GameTerminalException('Actions are not applicable to terminal games')
        elif self.chance != self.player.nature:
            raise GamePlayerException('Nature acts chance actions')

    def act(self):
        """
        Takes the action of the game. The inheriting action classes should override this method, call the super method,
        and make necessary updates to the game.
        :return: None
        """
        self._validate()

        if self.public:
            self.game.logs.append(Log(self))

    @property
    @abstractmethod
    def chance(self):
        """
        Returns whether or not the action is a chance action.
        :return: a boolean value of whether or not the action is a chance action
        """
        pass

    @property
    @abstractmethod
    def public(self):
        """
        Returns whether or not the action is public or not.
        :return: a boolean value of whether or not the action is a public
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Returns the string representation of the action.
        :return: the string representation of the game
        """
        pass


class SeqAction(Action, ABC):
    """
    This is a base class for all sequential actions in gameservice.
    """

    def _validate(self):
        """
        Validates the integrity of the sequential action.
        :return: None
        :raise GameTypeException: if the game is not a sequential game
        :raise GamePlayerException: if the player to act is not the acting player
        """
        super()._validate()

        if not isinstance(self.game, SeqGame):
            raise GameTypeException('The game is not a sequential game')
        if self.player is not self.game.player:
            raise GamePlayerException(f'{self.player} cannot act in turn')
