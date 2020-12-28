from unittest import TestCase, main

from gameframe.sequential.tests import SequentialTestCaseMixin
from gameframe.tictactoe import TicTacToeEnvironment, TicTacToeGame, TicTacToeNature, TicTacToePlayer


class TicTacToeTestCase(TestCase, SequentialTestCaseMixin[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature,
                                                          TicTacToePlayer]):
    """TicTacToeTestCase is the class for tic tac toe test cases."""

    def test_draw(self) -> None:
        """Tests if the tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        self.assertEqual([0, 0], [player.payoff for player in game.players])

    def test_loss(self) -> None:
        """Tests if the tic tac toe properly detects a case of the first player losing.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        self.assertEqual([-1, 1], [player.payoff for player in game.players])

    def test_win(self) -> None:
        """Tests if the tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        while not game.terminal:
            game.player.actions[0].act()

        self.assertEqual([1, -1], [player.payoff for player in game.players])

    @staticmethod
    def _create_game() -> TicTacToeGame:
        return TicTacToeGame()

    @staticmethod
    def _verify(game: TicTacToeGame) -> None:
        assert game.environment._winner is not None or not game.environment._empty_coordinates

    @property
    def _num_monte_carlo_tests(self) -> int:
        return 10000


if __name__ == '__main__':
    main()
