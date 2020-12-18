"""
This module defines tic tac toe test cases in gameservice.
"""
from unittest import TestCase, main

from gameservice.game.tests.testcasemixins import SeqTestCaseMixin
from gameservice.tictactoe import TTTGame


class TTTTestCase(TestCase, SeqTestCaseMixin):
    """
    This is a class for tic tac toe test cases.
    """

    @staticmethod
    def create_game():
        """
        Creates a tic tac toe game instance.
        :return: a tic tac toe game instance
        """
        return TTTGame()

    @staticmethod
    def validate_game(game):
        """
        Validates the integrity of the tic tac toe game.
        :param game: a tic tac toe game of the tic tac toe test case
        :return: a boolean value of the validity of the tic tac toe game
        """
        return game.environment.winner is not None or not game.environment.empty_coords

    @property
    def num_monte_carlo_tests(self):
        """
        :return: the number of monte carlo tests of tic tac toe games
        """
        return 10000

    def test_tic_tac_toe_first_win(self):
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

    def test_tic_tac_toe_second_win(self):
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

    def test_tic_tac_toe_draw(self):
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
