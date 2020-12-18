from abc import ABC, abstractmethod

import treys

from .hand import Hand


class Evaluator(ABC):
    @abstractmethod
    def hand(self, hole_cards, board):
        pass


class StandardEvaluator(Evaluator):
    def __init__(self):
        self.__evaluator = treys.Evaluator()

    def hand(self, hole_cards, board):
        card_ints = [treys.Card.new(str(card)) for card in hole_cards + board]

        try:
            return Hand(self.__evaluator.evaluate(card_ints, []))
        except KeyError:
            return None
