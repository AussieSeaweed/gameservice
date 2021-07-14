"""This module defines the abstract base classes for all components of games in GameFrame.

These components are as follows:

- Game
- Actor
- Action (internal)

All elements of games in GameFrame should inherit from the above classes.
"""
from abc import ABC, abstractmethod
from collections.abc import Iterator

from gameframe.exceptions import GameFrameError


class Game(ABC):
    """Game is the abstract base class for all games.

    Every game has to define its nature and players.

    :param nature: The nature of this game.
    :param players: The players of this game.
    """

    def __init__(self, nature, players):
        self._nature = nature
        self._players = list(players)

    @property
    def nature(self):
        """Returns the nature of this game.

        :return: The nature of this game.
        """
        return self._nature

    @property
    def players(self):
        """Returns the players of this game.

        :return: The players of this game.
        """
        return tuple(self._players)

    @abstractmethod
    def is_terminal(self):
        """Returns the terminal status of this game.

        :return: True if this game is terminal, else False.
        """
        ...


class Actor(Iterator):
    """Actor is the class for actors.

    :param game: The game of this actor.
    """

    def __init__(self, game):
        self._game = game

    def __next__(self):
        return self.game.players[(self.index + 1) % len(self.game.players)]

    @property
    def game(self):
        """Returns the game of this actor.

        :return: The game of this actor.
        """
        return self._game

    @property
    def index(self):
        """Returns the optional index of this actor.

        If this actor is the nature, None is returned.

        :return: None if this actor is the nature, else the index of this player.
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
        return self in self.game.players


class _Action(ABC):
    def __init__(self, actor):
        self.actor = actor

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
        if self.actor.game.is_terminal():
            raise GameFrameError('Actions can only be applied to non-terminal games')

    @abstractmethod
    def apply(self):
        ...
