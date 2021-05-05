from unittest import TestCase

from gameframe.tests.utilities import MonteCarloTestCaseMixin


class PokerTestMixin(MonteCarloTestCaseMixin[Poker]):
    pass


class NoLimitHoldEmTest(PokerTestMixin, TestCase):
    pass
