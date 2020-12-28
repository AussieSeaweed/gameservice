from abc import ABC, abstractmethod
from itertools import combinations
from typing import List, Optional

from .cards import Card
from .hands import Hand, _TreysHand


class Evaluator(ABC):
    """Evaluator is the abstract base class for all evaluators."""

    @abstractmethod
    def hand(self, hole_cards: List[Card], board_cards: List[Card]) -> Optional[Hand]:
        """Evaluates the hand of the combinations of the hole cards and the board cards.

        If the number of cards are insufficient, None is returned

        :param hole_cards: the hole cards
        :param board_cards: the board cards
        :return: None if the number of cards are insufficient, else the hand of the combinations
        """
        pass


class TexasHoldEmEvaluator(Evaluator):
    """TexasHoldEmEvaluator is the class for texas hold'em evaluators"""

    def hand(self, hole_cards: List[Card], board_cards: List[Card]) -> Optional[Hand]:
        if len(hole_cards) < 2 or len(hole_cards) + len(board_cards) < 5:
            return None
        else:
            return _TreysHand(hole_cards, board_cards)


class OmahaHoldEmEvaluator(TexasHoldEmEvaluator):
    """OmahaHoldEmEvaluator is the class for omaha hold'em evaluators"""

    def hand(self, hole_cards: List[Card], board_cards: List[Card]) -> Optional[Hand]:
        hand = None

        for combination in combinations(hole_cards, 2):
            if hand is None:
                hand = super().hand(combination, board_cards)
            else:
                hand = min(hand, super().hand(combination, board_cards))

        return hand
