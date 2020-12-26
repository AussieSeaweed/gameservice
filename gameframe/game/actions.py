"""
This module defines actions and sequential actions in gameframe.
"""
from abc import ABC, abstractmethod

from .exceptions import PlayerException, TerminalException, TypeException
from .games import SequentialGame
from .utils import Log


class Action(ABC):
    """
    This is a class that represents actions.
    """

    def __init__(self, player):
        self.__player = player

    @property
    def player(self):
        """
        :return: the acting player
        """
        return self.__player

    @property
    def game(self):
        """
        :return: the game of the action
        """
        return self.player.game

    def validate(self):
        """
        Validates the integrity of the action.

        :return: None
        :raise GameTerminalException: if the game is terminal
        :raise GamePlayerException: if the action is a chance action but the player is not nature or vice versa
        """

        if self.game.terminal:
            raise TerminalException('Actions are not applicable to terminal games')
        elif self.chance != self.player.nature:
            raise PlayerException('Nature acts chance actions')

    def act(self):
        """
        Applies the action to the associated game.

        The overridden act method should first call the super method and then make the necessary modifications to the
        game.

        :return: None
        :raise GameException: if game validation fails
        """
        self.validate()

        if self.public:
            self.game.logs.append(Log(self))

    @property
    @abstractmethod
    def chance(self):
        """
        :return: a boolean value of whether or not the action is a chance action
        """
        pass

    @property
    @abstractmethod
    def public(self):
        """
        :return: a boolean value of whether or not the action is public
        """
        pass

    @abstractmethod
    def __str__(self):
        pass


class SequentialAction(Action, ABC):
    """
    This is a class that represents sequential actions.
    """

    def validate(self):
        super().validate()

        if not isinstance(self.game, SequentialGame):
            raise TypeException('The game is not a sequential game')
        if self.player is not self.game.player:
            raise PlayerException(f'{self.player} cannot act in turn')
