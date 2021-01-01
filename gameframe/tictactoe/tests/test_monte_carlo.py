from __future__ import annotations

from unittest import TestCase, main

from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin
from gameframe.tictactoe import TicTacToeGame


class TicTacToeMonteCarloTestCase(TestCase, SequentialMonteCarloTestCaseMixin[TicTacToeGame]):
    """TicTacToeTestCase is the class for tic tac toe test cases."""

    def test_draw(self: TicTacToeMonteCarloTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[4].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([0, 0], [player.payoff for player in game.players])

    def test_loss(self: TicTacToeMonteCarloTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of the first player losing.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[8].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([-1, 1], [player.payoff for player in game.players])

    def test_win(self: TicTacToeMonteCarloTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([1, -1], [player.payoff for player in game.players])

    def _create_game(self: TicTacToeMonteCarloTestCase) -> TicTacToeGame:
        return TicTacToeGame()

    def _verify(self: TicTacToeMonteCarloTestCase, game: TicTacToeGame) -> None:
        assert game.environment._winner is not None or not game.environment._empty_coordinates

    @property
    def _num_monte_carlo_tests(self: TicTacToeMonteCarloTestCase) -> int:
        return 10000


if __name__ == '__main__':
    main()
