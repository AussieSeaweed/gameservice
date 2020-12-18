"""
This module defines a general game test in gameservice.
"""
from abc import ABC, abstractmethod
from random import choice
from unittest import TestCase


class GameTestCase(TestCase, ABC):
    """
    This is a base class for all game test cases in gameservice.
    """

    @staticmethod
    @abstractmethod
    def create_game():
        """
        Creates a game instance.
        :return: a game instance
        """
        pass

    @staticmethod
    @abstractmethod
    def check_game(game):
        """
        Checks the integrity of the game.
        :param game: a game to be checked on
        :return: None
        """
        pass


class SeqTestCase(GameTestCase, ABC):
    """
    This is a base class for all sequential game test cases in gameservice.
    """

    @property
    @abstractmethod
    def num_monte_carlo_tests(self):
        """
        Returns the number of monte carlo tests.
        :return: the number of monte carlo tests
        """
        pass

    def test_monte_carlo(self):
        """
        Runs monte carlo games.
        :return: None
        """
        for i in range(self.num_monte_carlo_tests):
            game = self.create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            assert self.check_game(game)
