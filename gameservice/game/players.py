"""
This module defines players and natures in gameservice.
"""
from abc import ABC, abstractmethod


class Player(ABC):
    """
    This is a class that represents players.
    """

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """
        :return: the game of the player
        """
        return self.__game

    @property
    def nature(self):
        """
        :return: a boolean value of whether or not the player is the nature
        """
        return self is self.game.nature

    @property
    def index(self):
        """
        :return: the index of the player
        """
        return None if self.nature else self.game.players.index(self)

    @property
    @abstractmethod
    def payoff(self):
        """
        :return: the payoff of the player
        """
        pass

    @property
    @abstractmethod
    def actions(self):
        """
        :return: a list of actions of the player
        """
        pass

    @property
    @abstractmethod
    def info_set(self):
        """
        :return: the info-set of the player
        """
        pass

    def __next__(self):
        """
        Finds the next player of the game unless the player is the nature, in which case the nature is returned.

        :return: the next player or the nature of the game
        """
        return self.game.nature if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        """
        Converts the player into a string representation.

        :return: the string representation of the player
        """
        return f'Player {self.index}'


class Nature(Player, ABC):
    """
    This is a class that represents natures.

    The nature's default payoff assumes that the game is a zero sum game and returns the negated sum of the players'
    payoffs.
    """

    @property
    def payoff(self):
        return -sum(player.payoff for player in self.game.players)

    def __str__(self):
        return 'Nature'
