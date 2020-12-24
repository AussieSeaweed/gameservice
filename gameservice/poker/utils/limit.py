"""
This module defines limits in gameservice.
"""
from abc import ABC, abstractmethod


class Limit(ABC):
    """
    This is a class that represents limits.
    """

    @abstractmethod
    def bet_amounts(self, player):
        """
        Determines the bet amounts the betting player can make

        :param player: the betting player
        :return: a list of bet amounts the player can make
        """
        pass


class NoLimit(Limit):
    """
    This is a class that represents no-limits.
    """

    def bet_amounts(self, player):
        amounts = []

        if sum(player.relevant for player in player.game.players) > 1:
            max_bet = max(player.bet for player in player.game.players)

            if max_bet + player.game.environment.min_raise < player.total:
                amounts.extend(self.int_bet_amounts(max_bet + player.game.environment.min_raise, player.total))
            elif max_bet < player.total:
                amounts.append(player.total)

        return amounts

    def int_bet_amounts(self, min_amount, max_amount):
        """
        :param min_amount: the minimum bet amount
        :param max_amount: the maximum bet amount
        :return: a list of bet amounts within the interval
        """
        return list(range(min_amount, max_amount + 1))


class LazyNoLimit(NoLimit):
    """
    This is a class that represents lazy no-limits.
    """

    def int_bet_amounts(self, min_amount, max_amount):
        return list({min_amount, max_amount})
