"""
This module defines test case mixins and sequential test case mixins in gameservice.
"""
from abc import ABC, abstractmethod
from random import choice


class TestCaseMixin(ABC):
    """
    This is a mixin for game test cases.
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
    def validate_game(game):
        """
        Validates the integrity of the game.

        :param game: a game of the test case
        :return: a boolean value of the validity of the game
        """
        pass


class SeqTestCaseMixin(TestCaseMixin, ABC):
    """
    This is a mixin for sequential test cases.
    """

    @property
    @abstractmethod
    def num_monte_carlo_tests(self):
        """
        :return: the number of monte carlo tests of sequential games
        """
        pass

    def test_monte_carlo(self):
        """
        Runs monte carlo tests of sequential games.

        :return: None
        :raise AssertionError: if the game validation fails in any tests
        """
        for i in range(self.num_monte_carlo_tests):
            game = self.create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            assert self.validate_game(game)
