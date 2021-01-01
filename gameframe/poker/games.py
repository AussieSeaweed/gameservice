from abc import ABC

from gameframe.poker.bases import PokerGame
from gameframe.poker.utils.decks import StandardDeck
from gameframe.poker.utils.evaluators import GreekHoldEmEvaluator, OmahaHoldEmEvaluator, StandardEvaluator


class CommunityCardGame(PokerGame, ABC):
    """CommunityCardGame is the abstract base class for all community card games."""
    pass


class TexasHoldEmGame(CommunityCardGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return StandardEvaluator()


class OmahaHoldEmGame(CommunityCardGame, ABC):
    """OmahaHoldEmGame is the abstract base class for all omaha hold'em games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return OmahaHoldEmEvaluator()


class GreekHoldEmGame(CommunityCardGame, ABC):
    """GreekHoldEmGame is the abstract base class for all greek hold'em games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return GreekHoldEmEvaluator()


class DrawGame(PokerGame, ABC):
    """DrawGame is the abstract base class for all draw games."""
    pass


class FiveCardDraw(PokerGame, ABC):
    """FiveCardDraw is the abstract base class for all five card draw games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return StandardEvaluator()
