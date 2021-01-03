from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, final

from gameframe.utils import override

if TYPE_CHECKING:
    from gameframe.poker import PokerGame


class Limit(ABC):
    """Limit is the abstract base class for all limits."""

    def __init__(self, game: PokerGame) -> None:
        self.__game: PokerGame = game

    @property
    @final
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
                   self.game.actor._total)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        """
        :return: the maximum bet amount
        """
        pass


@final
class NoLimit(Limit):
    """NoLimit is the class for no-limits."""

    @property
    @override
    def max_amount(self) -> int:
        return self.game.actor._total
