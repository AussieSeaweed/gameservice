"""
This module defines streets in gameframe.
"""


class Street:
    """
    This is a class that represents streets.
    """

    def __init__(self, num_hole_cards, num_board_cards):
        self.__num_hole_cards = num_hole_cards
        self.__num_board_cards = num_board_cards

    @property
    def num_hole_cards(self):
        """
        :return: the number of hole cards to be dealt in the beginning of the street
        """
        return self.__num_hole_cards

    @property
    def num_board_cards(self):
        """
        :return: the number of board cards to be dealt in the beginning of the street
        """
        return self.__num_board_cards
