from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC

from gameframe.poker.bases import PokerGame
from gameframe.poker.utils import StandardDeck, GreekHoldEmEvaluator, OmahaHoldEmEvaluator, StandardEvaluator

if TYPE_CHECKING:
    from . import Round


class CommunityCardGame(PokerGame, ABC):
    """CommunityCardGame is the abstract base class for all community card games."""

    def _create_rounds(self: CommunityCardGame) -> list[Round]:
        pass


class TexasHoldEmGame(CommunityCardGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def _create_deck(self: TexasHoldEmGame) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self: TexasHoldEmGame) -> StandardEvaluator:
        return StandardEvaluator()


class OmahaHoldEmGame(CommunityCardGame, ABC):
    """OmahaHoldEmGame is the abstract base class for all omaha hold'em games."""

    def _create_deck(self: OmahaHoldEmGame) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self: OmahaHoldEmGame) -> OmahaHoldEmEvaluator:
        return OmahaHoldEmEvaluator()


class GreekHoldEmGame(CommunityCardGame, ABC):
    """GreekHoldEmGame is the abstract base class for all greek hold'em games."""

    def _create_deck(self: GreekHoldEmGame) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self: GreekHoldEmGame) -> GreekHoldEmEvaluator:
        return GreekHoldEmEvaluator()


class DrawGame(PokerGame, ABC):
    """DrawGame is the abstract base class for all draw games."""

    def _create_rounds(self: DrawGame) -> list[Round]:
        pass


class FiveCardDraw(PokerGame, ABC):
    """FiveCardDraw is the abstract base class for all five card draw games."""

    def _create_deck(self: FiveCardDraw) -> StandardDeck:
        return StandardDeck()

    def _create_evaluator(self: FiveCardDraw) -> StandardEvaluator:
        return StandardEvaluator()
