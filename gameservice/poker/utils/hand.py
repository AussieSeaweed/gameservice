"""
This module defines hands in gameservice.
"""
from .treys_utils import rank_to_str


class Hand:
    """
    This is a class that represents hands.
    """

    def __init__(self, hand_rank):
        self.__hand_rank = hand_rank

    def __lt__(self, other):
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other):
        return self.__hand_rank == other.__hand_rank

    def __hash__(self):
        return hash(self.__hand_rank)

    def __str__(self):
        return f'{self.__hand_rank} ({rank_to_str(self.__hand_rank)})'
