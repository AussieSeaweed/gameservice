"""
This module defines tic tac toe test cases in gameservice.
"""
from unittest import TestCase, main

from gameservice.game.tests.testcasemixins import SequentialTestCaseMixin
from gameservice.tictactoe import TicTacToeGame


class TicTacToeTestCase(TestCase, SequentialTestCaseMixin):
    """
    This is a class for tic tac toe test cases.
    """

    @staticmethod
    def create_game():
        return TicTacToeGame()

    @staticmethod
    def validate_game(game):
        return game.environment.winner is not None or not game.environment.empty_coords

    @property
    def num_monte_carlo_tests(self):
        return 10000

    def test_first_win(self):
        """
        Tests if the tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game = self.create_game()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([1, -1], payoffs)

    def test_second_win(self):
        """
        Tests if the tic tac toe properly detects a case of the second player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game = self.create_game()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([-1, 1], payoffs)

    def test_draw(self):
        """
        Tests if the tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game = self.create_game()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([0, 0], payoffs)


if __name__ == '__main__':
    main()
