from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from gameframe.poker.bases import PokerGame
from gameframe.poker.limits import NoLimit
from gameframe.poker.rounds import BettingRound
from gameframe.poker.utils import StandardDeck, StandardEvaluator

if TYPE_CHECKING:
    from gameframe.poker import Round


class NoLimitMixin(PokerGame, ABC):
    """NoLimitMixin is the mixin for no-limit poker."""

    def _create_limit(self) -> NoLimit:
        return NoLimit(self)


class HoldEmGame(PokerGame, ABC):
    """HoldEmGame is the abstract base class for all hold'em games."""

    @property
    @abstractmethod
    def _hole_card_count(self) -> int:
        pass

    @property
    @abstractmethod
    def _board_card_counts(self) -> list[int]:
        pass

    def _create_rounds(self) -> list[Round]:
        return [BettingRound(self, 0, [False] * self._hole_card_count)] + list(map(
            lambda board_card_count: BettingRound(self, board_card_count, []), self._board_card_counts))


class TexasHoldEmGame(HoldEmGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    @property
    def _hole_card_count(self) -> int:
        return 2

    @property
    def _board_card_counts(self) -> list[int]:
        return [3, 1, 1]

    def _create_deck(self) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self) -> StandardEvaluator:
        return StandardEvaluator()


class NoLimitTexasHoldEmGame(TexasHoldEmGame, NoLimitMixin, ABC):
    """NoLimitTexasHoldEmGame is the abstract base class for all no-limit texas hold'em games."""
