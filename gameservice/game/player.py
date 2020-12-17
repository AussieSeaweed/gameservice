"""
This module defines a general player of gameservice.
"""
from abc import ABC, abstractmethod


class Player(ABC):
    """
    This is a base class for all players in gameservice.
    """

    def __init__(self, game, label=None):
        """
        Constructs the Player instance.
        :param game: the game of the player
        :param label: the optional string label of the player
        """
        self.__game = game
        self.__label = label

    @property
    def game(self):
        """
        Returns the game of the player.
        :return: the game of the player
        """
        return self.__game

    @property
    def label(self):
        """
        Returns the label of the player.
        :return: the label of the player
        """
        return self.__label

    @property
    def nature(self):
        """
        Returns whether or not the player is the nature.
        :return: a boolean value of whether or not the player is the nature
        """
        return self is self.game.nature

    @property
    def index(self):
        """
        Returns the index of the player.
        :return: the index of the player
        """
        return None if self.nature else self.game.players.index(self)

    @property
    @abstractmethod
    def payoff(self):
        """
        Returns the payoff of the player.
        :return: the payoff of the player
        """
        pass

    @property
    @abstractmethod
    def actions(self):
        """
        Returns the actions that the player can take in the game at the current state.
        :return: a list of the actions of the player
        """
        pass

    @property
    @abstractmethod
    def info_set(self):
        """
        Returns the info-set of the player.
        :return: the info-set of the player
        """
        pass

    def __next__(self):
        """
        Returns the next player of the game unless the player is the nature, in which case the nature (the same player)
        is returned.
        :return: the next player or the nature of the game
        """
        return self.game.nature if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self):
        """
        Returns the string representation of the player.
        :return: the string representation of the player
        """
        return f'Player {self.index}' if self.label is None else self.label


class Nature(Player, ABC):
    @property
    def payoff(self):
        """
        Returns the negated sum of the player payoffs in the game which is the default nature payoff.
        :return: the default nature payoff
        """
        return -sum(player.payoff for player in self.game.players)

    def __str__(self):
        """
        Returns the string representation of the nature.
        :return: the string representation of the nature
        """
        return 'Nature'
