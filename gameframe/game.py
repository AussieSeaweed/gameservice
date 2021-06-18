"""This module defines the abstract base classes for all components of games in GameFrame.

These components are as follows:

- Game
- Actor
- Action (internal)

All elements of games in GameFrame should inherit from the above classes.
"""
from abc import ABC, abstractmethod

from gameframe.exceptions import GameFrameError


class Game(ABC):
    """Game is the abstract base class for all games.

    Every game has to define its nature and players.

    :param nature: The nature of this game.
    :param players: The players of this game.
    """

    def __init__(self, nature, players):
        self.__nature = nature
        self.__players = tuple(players)

    @property
    def nature(self):
        """Returns the nature of this game.

        :return: The nature of this game.
        """
        return self.__nature

    @property
    def players(self):
        """Returns the players of this game.

        :return: The players of this game.
        """
        return self.__players

    @abstractmethod
    def is_terminal(self):
        """Returns the terminal status of this game.

        :return: True if this game is terminal, else False.
        """
        ...


class Actor:
    """Actor is the class for actors.

    :param game: The game of this actor.
    """

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """Returns the game of this actor.

        :return: The game of this actor.
        """
        return self.__game

    @property
    def index(self):
        """Returns the optional index of this actor.

        If this actor is the nature, None is returned.

        :return: The optional index of this actor.
        """
        return None if self.is_nature() else self.game.players.index(self)

    def is_nature(self):
        """Returns whether or not if this actor is the nature.

        :return: True if this actor is the nature, else False.
        """
        return self is self.game.nature

    def is_player(self):
        """Returns whether or not if this actor is one of the players.

        :return: True if this actor is one of the players, else False.
        """
        return self is not self.game.nature


class _Action(ABC):
    def __init__(self, actor):
        self.actor = actor

    @property
    def game(self):
        return self.actor.game

    def act(self):
        self.verify()
        self.apply()

    def can_act(self):
        try:
            self.verify()
        except GameFrameError:
            return False
        else:
            return True

    def verify(self):
        if not isinstance(self.actor, Actor):
            raise GameFrameError('The supplied actor must be a valid actor')
        elif self.game.is_terminal():
            raise GameFrameError('Actions can only be applied to non-terminal games')

    @abstractmethod
    def apply(self):
        ...
