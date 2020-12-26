"""
This module defines evaluators in gameframe.
"""
from abc import ABC, abstractmethod

from .hand import Hand
from .treys_utils import evaluate


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

    def hand(self, hole_cards, board):
        if len(hole_cards) + len(board) >= 5:
            card_strs = list(map(str, hole_cards + board))

            return Hand(evaluate(card_strs))
        else:
            return None
