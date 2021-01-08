from abc import ABC, abstractmethod

from gameframe.game.exceptions import TerminalGameException


class Action(ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, actor):
        self._actor = actor

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def public(self):
        """
        :return: True if this action is a public action, False otherwise
        """
        pass

    @property
    def _game(self):
        return self._actor._game

    def act(self):
        """Applies this action to the game.

        The overridden act method should first call the super method and then make the changes in the game.

        :return: None
        :raise GameFrameException: if the action integrity verification fails prior to the application of this action
        """
        self._verify()

    def _verify(self):
        if self._game.terminal:
            raise TerminalGameException()
