"""
This module defines poker_ environments in gameframe.
"""
from ..game import Environment


class PokerEnvironment(Environment):
    """
    This is a class that represents poker_ environments.
    """

    def __init__(self, game):
        super().__init__(game)

        self.aggressor = None
        self.min_delta = None

        self.pot = 0
        self.__board = []

    @property
    def board(self):
        """
        :return: the board of the poker_ environment
        """
        return self.__board
