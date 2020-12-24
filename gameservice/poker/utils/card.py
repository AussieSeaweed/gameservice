"""
This module defines cards in gameservice.
"""


class Card:
    """
    This is a class that represents cards.
    """

    def __init__(self, card_str):
        self.__card_str = card_str

    def __str__(self):
        """
        Converts the card into a string representation.

        :return: the string representation of the card
        """
        return self.__card_str
