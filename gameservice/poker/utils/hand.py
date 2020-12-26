"""
This module defines hands in gameservice.
"""
from treys.evaluator import Evaluator


class Hand:
    """
    This is a class that represents hands.
    """

    def __init__(self, hand_rank):
        self.__hand_rank = hand_rank
        self.__evaluator = Evaluator()

    def __lt__(self, other):
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other):
        return self.__hand_rank == other.__hand_rank

    def __hash__(self):
        return hash(self.__hand_rank)

    def __str__(self):
        return f'{self.__hand_rank} (' \
               f'{self.__evaluator.class_to_string(self.__evaluator.get_rank_class(self.__hand_rank))})'
