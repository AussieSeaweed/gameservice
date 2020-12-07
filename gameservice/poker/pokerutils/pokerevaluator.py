from abc import ABC, abstractmethod

from treys import Card, Evaluator

from .pokerhand import PokerHand


class PokerEvaluator(ABC):
    @abstractmethod
    def hand(self, hole_cards, board):
        pass


class PokerStdEvaluator(PokerEvaluator):
    def __init__(self):
        self.__evaluator = Evaluator()

    def hand(self, hole_cards, board):
        card_ints = [Card.new(str(card)) for card in hole_cards + board]

        try:
            return PokerHand(self.__evaluator.evaluate(card_ints, []))
        except KeyError:
            return None
