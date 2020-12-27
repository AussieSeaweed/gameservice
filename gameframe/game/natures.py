from abc import ABC

from .players import Player


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
