from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameframe.poker import PokerGame


class Limit(ABC):
    """Limit is the abstract base class for all limits."""

    def __init__(self, game: PokerGame) -> None:
        self.__game: PokerGame = game

    @property
    def game(self) -> PokerGame:
        """
        :return: the game of the round
        """
        return self.__game

    @property
    def min_amount(self) -> int:
        """
        :return: the minimum bet amount
        """
        return min(max(player.bet for player in self.game.players) + self.game.environment._max_delta,
                   self.game.actor.total)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        """
        :return: the maximum bet amount
        """
        pass


class NoLimit(Limit):
    """NoLimit is the class for no-limits."""

    @property
    def max_amount(self) -> int:
        return self.game.actor.total


class FixedLimit(Limit):
    """FixedLimit is the class for fixed limits."""

    @property
    def max_amount(self) -> int:
        return self.min_amount
