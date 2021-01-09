from abc import ABC, abstractmethod


class Limit(ABC):
    """Limit is the abstract base class for all limits."""

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """
        :return: the game of this limit
        """
        return self.__game

    @property
    def min_amount(self):
        """
        :return: the minimum bet/raise amount
        """
        return min(max(player.bet for player in self.game.players) + self.game.environment.max_delta,
                   self.game.actor.total)

    @property
    @abstractmethod
    def max_amount(self):
        """
        :return: the maximum bet/raise amount
        """
        pass


class NoLimit(Limit):
    """NoLimit is the class for no-limits."""

    @property
    def max_amount(self):
        return self.game.actor.total
