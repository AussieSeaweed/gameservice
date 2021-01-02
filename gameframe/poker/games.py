from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from gameframe.poker.bases import PokerGame
from gameframe.poker.utils import StandardDeck, StandardEvaluator

if TYPE_CHECKING:
    from gameframe.poker import Round


class HoldEmGame(PokerGame, ABC):
    """HoldEmGame is the abstract base class for all hold'em games."""

    def _create_rounds(self) -> list[Round]:
        return []  # TODO


class TexasHoldEmGame(HoldEmGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def _create_deck(self) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self) -> StandardEvaluator:
        return StandardEvaluator()
