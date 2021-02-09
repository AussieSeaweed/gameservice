from abc import ABC, abstractmethod
from collections import Collection
from itertools import combinations

from gameframe.poker.utils.cards import Card
from gameframe.poker.utils.hands import Hand, TreysHand


class Evaluator(ABC):
    """Evaluator is the abstract base class for all evaluators."""

    @abstractmethod
    def hand(self, hole_cards: Collection[Card], board_cards: Collection[Card]) -> Hand:
        """Evaluates the hand of the combinations of the hole cards and the board cards.

        If the number of cards are insufficient, None is returned

        :param hole_cards: the hole cards
        :param board_cards: the board cards
        :return: None if the number of cards are insufficient, else the hand of the combinations
        """
        pass


class StandardEvaluator(Evaluator):
    """StandardEvaluator is the class for standard evaluators."""

    def hand(self, hole_cards: Collection[Card], board_cards: Collection[Card]) -> Hand:
        if len(hole_cards) + len(board_cards) < 5:
            raise ValueError('Insufficient number of cards')
        else:
            return TreysHand(hole_cards, board_cards)


class GreekEvaluator(StandardEvaluator):
    """GreekEvaluator is the class for Greek evaluators."""

    def hand(self, hole_cards: Collection[Card], board_cards: Collection[Card]) -> Hand:
        hand = super().hand

        return max(hand(hole_cards, combination) for combination in combinations(board_cards, 3))


class OmahaEvaluator(GreekEvaluator):
    """OmahaEvaluator is the class for Omaha evaluators."""

    def hand(self, hole_cards: Collection[Card], board_cards: Collection[Card]) -> Hand:
        hand = super().hand

        return max(hand(combination, board_cards) for combination in combinations(hole_cards, 2))
