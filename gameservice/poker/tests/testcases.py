"""
This module defines no-limit texas hold'em test cases in gameservice.
"""
from unittest import TestCase

from gameservice.poker.tests.testcasemixins import PokerTestCaseMixin
from gameservice.poker import LazyNLHEGame


class CustomNLHEGame(LazyNLHEGame):
    """
    This is a class for custom 9-max no-limit texas hold'em games.
    """

    @property
    def ante(self):
        return 1

    @property
    def blinds(self):
        return [1, 2]

    @property
    def starting_stacks(self):
        return [200, 300, 500, 500, 200, 300, 1000, 500, 500]


class NLHETestCase(TestCase, PokerTestCaseMixin):
    """
    This is a class for no-limit texas hold'em game test cases.
    """

    @staticmethod
    def create_game():
        return CustomNLHEGame()
