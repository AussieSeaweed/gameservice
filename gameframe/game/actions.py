from abc import ABC, abstractmethod

from gameframe.game.exceptions import ActionException


class Action(ABC):
    """Action is the abstract base class for all actions."""

    def __init__(self, actor):
        self.__actor = actor

    @abstractmethod
    def __str__(self):
        pass

    @property
    def actor(self):
        """
        :return: the actor of this action
        """
        return self.__actor

    @property
    def game(self):
        """
        :return: the game of this action
        """
        return self.actor.game

    @property
    def applicable(self):
        """
        :return: True if this action can be applied else False
        """
        return not self.game.terminal

    @property
    @abstractmethod
    def public(self):
        """
        :return: True if this action is a public action, False otherwise
        """
        pass

    def act(self):
        """Applies this action to the game.

        The overridden act method should first call the super method and then make the changes in the game.

        :return: None
        :raise ActionException: if the action cannot be applied
        """
        if not self.applicable:
            raise ActionException()
