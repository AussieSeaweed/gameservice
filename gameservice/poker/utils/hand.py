"""
This module defines hands in gameservice.
"""


class Hand:
    """
    This is a class that represents hands.
    """

    def __init__(self, hand_rank):
        self.__hand_rank = hand_rank

    def __lt__(self, other):
        """
        Determines the superiority of the hand against another hand.

        :param other: another hand to be compared against
        :return: a boolean value of whether or not the hand is superior to the other hand
        """
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other):
        """
        Determines the equality of the hand against another hand.

        :param other: another hand to be compared against
        :return: a boolean value of whether or not the hand is equal to the other hand
        """
        return self.__hand_rank == other.__hand_rank

    def __hash__(self):
        """
        :return: the hash value of the hand
        """
        return hash(self.__hand_rank)
