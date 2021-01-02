from typing import final
from unittest import TestCase, main

from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin
from gameframe.tictactoe import TicTacToeGame
from gameframe.utils import override


@final
class TicTacToeMonteCarloTestCase(TestCase, SequentialMonteCarloTestCaseMixin[TicTacToeGame]):
    """TicTacToeTestCase is the class for tic tac toe test cases."""

    _test_count: int = 10000

    def test_draw(self) -> None:
        """Tests if tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[4].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertSequenceEqual((0, 0), tuple(map(lambda player: player.payoff, game.players)))

    def test_loss(self) -> None:
        """Tests if tic tac toe properly detects a case of the first player losing.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[8].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertSequenceEqual((-1, 1), tuple(map(lambda player: player.payoff, game.players)))

    def test_win(self) -> None:
        """Tests if tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertSequenceEqual((1, -1), tuple(map(lambda player: player.payoff, game.players)))

    @override
    def _create_game(self) -> TicTacToeGame:
        return TicTacToeGame()

    @override
    def _verify_game(self, game: TicTacToeGame) -> None:
        assert game.environment._winner is not None or not game.environment._empty_coordinates


if __name__ == '__main__':
    main()
