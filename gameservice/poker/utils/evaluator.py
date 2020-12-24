"""
This module defines evaluators in gameservice.
"""
from abc import ABC, abstractmethod

import treys

from .hand import Hand


class Evaluator(ABC):
    """
    This is a class that represents evaluators.
    """

    @abstractmethod
    def hand(self, hole_cards, board):
        """
        Evaluates the hand of the combination of the hole_cards and the board.

        :param hole_cards: the hole cards of the poker player
        :param board: the board of the poker environment
        :return: the hand of the combination of the hole_cards and the board
        """
        pass


class StandardEvaluator(Evaluator):
    """
    This is a class that represents standard evaluators.
    """

    def __init__(self):
        self.__evaluator = treys.Evaluator()

    def hand(self, hole_cards, board):
        card_ints = [treys.Card.new(str(card)) for card in hole_cards + board]

        try:
            return Hand(self.__evaluator.evaluate(card_ints, []))
        except KeyError:
            return None
