from unittest import TestCase, main

from gameframe.sequential.tests import MCTestCaseMixin
from gameframe.tictactoe import TTTGame


class TTTMonteCarloTestCase(TestCase, MCTestCaseMixin[TTTGame]):
    """TTTMonteCarloTestCase is the class for tic tac toe test cases."""

    @property
    def _test_count(self) -> int:
        return 10000

    def _create_game(self) -> TTTGame:
        return TTTGame()

    def _verify(self, game: TTTGame) -> None:
        super()._verify(game)

        if game.is_terminal:
            assert game.env.winner is not None or not game.env.empty_coords
        else:
            assert game.env.winner is None and game.env.empty_coords


if __name__ == '__main__':
    main()
