"""
This module defines poker environments in gameservice.
"""
from ..game import Environment


class PokerEnvironment(Environment):
    """
    This is a class that represents poker environments.
    """

    def __init__(self, game):
        super().__init__(game)

        self.aggressor = None
        self.min_raise = None

        self.pot = 0
        self.__board = []

    @property
    def board(self):
        """
        :return: the board of the poker environment
        """
        return self.__board
