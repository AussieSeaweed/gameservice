from unittest import TestCase

from gameservice.game.tests.testmixin import SeqTestCaseMixin
from gameservice.tictactoe import TTTGame


class TTTTestCase(TestCase, SeqTestCaseMixin):
    @staticmethod
    def create_game():
        return TTTGame()

    @staticmethod
    def check_game(game):
        return game.winner is not None or not game.empty_coords

    @property
    def num_monte_carlo_tests(self):
        return 1000

    def test_tic_tac_toe_first_win(self):
        game = self.create_game()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([1, -1], payoffs)

    def test_tic_tac_toe_second_win(self):
        game = self.create_game()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([-1, 1], payoffs)

    def test_tic_tac_toe_draw(self):
        game = self.create_game()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([0, 0], payoffs)
