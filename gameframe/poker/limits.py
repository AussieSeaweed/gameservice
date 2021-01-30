from abc import ABC

from gameframe.poker.bases import PokerPlayer


class Limit(ABC):
    """Limit is the abstract base class for all limits."""

    @staticmethod
    def min_amount(player: PokerPlayer) -> int:
        """
        :return: the minimum bet/raise amount
        """
        return min(max(player.bet for player in player._game.players) + player._game.env._max_delta,
                   player.bet + player.stack)

    @staticmethod
    def max_amount(player: PokerPlayer) -> int:
        """
        :return: the maximum bet/raise amount
        """
        pass


class NoLimit(Limit):
    """NoLimit is the class for no-limits."""

    @staticmethod
    def max_amount(player: PokerPlayer) -> int:
        return player.bet + player.stack
