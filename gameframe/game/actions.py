from abc import ABC, abstractmethod


class Action(ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, player):
        self.__player = player

    @property
    def game(self):
        """
        :return: the game of the action
        """
        return self.player.game

    @property
    def player(self):
        """
        :return: the player of the action
        """
        return self.__player

    def act(self):
        """Applies the action to the game of the action.

        The overridden act method should first call the super method and then make the necessary modifications to the
        game.

        :return: None
        :raise ValueError: if the action integrity verification fails prior to the action
        """
        self._verify()

    @property
    @abstractmethod
    def chance(self):
        """
        :return: True if the action is a chance action, False otherwise
        """
        pass

    @property
    @abstractmethod
    def public(self):
        """
        :return: True if the action is a public action, False otherwise
        """
        pass

    @abstractmethod
    def __str__(self):
        pass

    def _verify(self):
        if self.game.terminal:
            raise ValueError('Actions are not applicable to terminal games')
        elif self.chance != self.player.nature:
            raise ValueError('Nature acts chance actions')
