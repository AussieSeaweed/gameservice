"""
This module defines tic tac toe test cases in gameframe.
"""
from unittest import main
from typing import List

from gameframe.sequential.tests import SequentialTestCase
from gameframe.tictactoe import TicTacToeEnvironment, TicTacToeGame, TicTacToeNature, TicTacToePlayer


class TicTacToeTestCase(SequentialTestCase[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer]):
    """
    This is a class for tic tac toe test cases.
    """

    @staticmethod
    def _create_game() -> TicTacToeGame:
        return TicTacToeGame()

    @staticmethod
    def _verify(game: TicTacToeGame) -> None:
        assert game.environment.winner is not None or not game.environment.empty_coords

    @property
    def _num_monte_carlo_tests(self) -> int:
        return 10000

    def test_first_win(self) -> None:
        """
        Tests if the tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs: List[int] = [player.payoff for player in game.players]

        self.assertEqual([1, -1], payoffs)

    def test_second_win(self) -> None:
        """
        Tests if the tic tac toe properly detects a case of the second player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs: List[int] = [player.payoff for player in game.players]

        self.assertEqual([-1, 1], payoffs)

    def test_draw(self) -> None:
        """
        Tests if the tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs: List[int] = [player.payoff for player in game.players]

        self.assertEqual([0, 0], payoffs)


if __name__ == '__main__':
    main()
