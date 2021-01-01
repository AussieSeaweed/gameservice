from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from gameframe.poker import PokerGame, PokerAction


class Round(ABC):
    """Round is the abstract base class for all rounds."""

    def __init__(self: Round, game: PokerGame) -> None:
        self.__game: PokerGame = game

    @property
    def game(self: Round) -> PokerGame:
        """
        :return: the game of the round
        """
        return self.__game

    @abstractmethod
    def _create_actions(self: Round) -> list[PokerAction]:
        pass


class BettingRound(Round, ABC):
    """BettingRound is the abstract base class for all betting rounds."""


class LimitBettingRound(BettingRound):
    """LimitBettingRound is the class for limit betting rounds."""
    pass


class PotLimitBettingRound(BettingRound):
    """PotLimitBettingRound is the class for pot-limit betting rounds."""
    pass


class NoLimitBettingRound(BettingRound):
    """NoLimitBettingRound is the class for no-limit betting rounds."""
    pass


class DrawingRound(Round):
    """DrawingRound is the class for drawing rounds."""
    pass


class SetupRound(Round):
    """SetupRound is the class for setup rounds."""
    pass
