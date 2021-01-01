from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import combinations
from typing import Optional

from gameframe.utils.cards import Card
from gameframe.utils.hands import Hand
from .hands import _TreysHand


class Evaluator(ABC):
    """Evaluator is the abstract base class for all evaluators."""

    @abstractmethod
    def hand(self: Evaluator, hole_cards: list[Card], board_cards: list[Card]) -> Optional[Hand]:
        """Evaluates the hand of the combinations of the hole cards and the board cards.

        If the number of cards are insufficient, None is returned

        :param hole_cards: the hole cards
        :param board_cards: the board cards
        :return: None if the number of cards are insufficient, else the hand of the combinations
        """
        pass


class StandardEvaluator(Evaluator):
    """StandardEvaluator is the class for standard evaluators"""

    def hand(self: StandardEvaluator, hole_cards: list[Card], board_cards: list[Card]) -> Optional[Hand]:
        if len(hole_cards) + len(board_cards) < 5:
            return None
        else:
            return _TreysHand(hole_cards, board_cards)


class OmahaHoldEmEvaluator(StandardEvaluator):
    """OmahaHoldEmEvaluator is the class for omaha hold'em evaluators"""

    def hand(self: OmahaHoldEmEvaluator, hole_cards: list[Card], board_cards: list[Card]) -> Optional[Hand]:
        hand: Optional[Hand] = None

        for combination in combinations(hole_cards, 2):
            cur_hand: Optional[Hand] = super().hand(combination, board_cards)

            if hand is None:
                hand: Optional[Hand] = cur_hand
            elif cur_hand is not None:
                hand: Optional[Hand] = max(hand, cur_hand)

        return hand


class GreekHoldEmEvaluator(StandardEvaluator):
    """GreekHoldEmEvaluator is the class for greek hold'em evaluators"""

    def hand(self: GreekHoldEmEvaluator, hole_cards: list[Card], board_cards: list[Card]) -> Optional[Hand]:
        hand: Optional[Hand] = None

        for combination in combinations(board_cards, 3):
            cur_hand: Optional[Hand] = super().hand(hole_cards, combination)

            if hand is None:
                hand: Optional[Hand] = cur_hand
            elif cur_hand is not None:
                hand: Optional[Hand] = max(hand, cur_hand)

        return hand
