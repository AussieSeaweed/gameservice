from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC

from gameframe.poker.bases import PokerGame
from gameframe.poker.utils import StandardDeck, StandardEvaluator

if TYPE_CHECKING:
    from gameframe.poker import Round


class CommunityCardGame(PokerGame, ABC):
    """CommunityCardGame is the abstract base class for all community card games."""

    def _create_rounds(self: CommunityCardGame) -> list[Round]:
        return []  # TODO


class TexasHoldEmGame(CommunityCardGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def _create_deck(self: TexasHoldEmGame) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self: TexasHoldEmGame) -> StandardEvaluator:
        return StandardEvaluator()
