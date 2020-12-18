from unittest import TestCase

from gameservice.game.tests.testmixin import SeqTestCaseMixin
from gameservice.tictactoe import TTTGame


class TTTTestCase(TestCase, SeqTestCaseMixin):
    """
    This is a class for tic tac toe game unit tests in gameservice.
    """

    @staticmethod
    def create_game():
        """
        Creates a tic tac toe game instance.
        :return: a tic tac toe game instance
        """
        return TTTGame()

    @staticmethod
    def check_game(game):
        """
        Checks the integrity of the tic tac toe game.
        :param game: a tic tac toe game to be checked on
        :return: None
        """
        return game.winner is not None or not game.empty_coords

    @property
    def num_monte_carlo_tests(self):
        """
        Returns the number of monte carlo tests of tic tac toe games.
        :return: the number of monte carlo tests of tic tac toe games
        """
        return 10000

    def test_tic_tac_toe_first_win(self):
        """
        Tests whether if the tic tac toe properly detects a case of the first player winning.
        :return: None
        """
        game = self.create_game()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([1, -1], payoffs)

    def test_tic_tac_toe_second_win(self):
        """
        Tests whether if the tic tac toe properly detects a case of the second player winning.
        :return: None
        """
        game = self.create_game()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([-1, 1], payoffs)

    def test_tic_tac_toe_draw(self):
        """
        Tests whether if the tic tac toe properly detects a case of a tied game.
        :return: None
        """
        game = self.create_game()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([0, 0], payoffs)
