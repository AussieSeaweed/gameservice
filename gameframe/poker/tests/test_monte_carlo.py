from unittest import TestCase, main

from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin
# TODO

class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, SequentialMonteCarloTestCaseMixin[TicTacToeGame]):
    """TicTacToeTestCase is the class for tic tac toe test cases."""

    @property
    def _monte_carlo_test_count(self) -> int:
        return 1000

    def _create_game(self) -> TicTacToeGame:
        return TicTacToeGame()

    def _verify_game(self, game: TicTacToeGame) -> None:
        assert game.environment._winner is not None or not game.environment._empty_coordinates


if __name__ == '__main__':
    main()
