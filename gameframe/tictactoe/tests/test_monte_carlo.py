from unittest import TestCase, main

from gameframe.sequential import SeqGame
from gameframe.sequential.tests import MCTestCaseMixin
from gameframe.tictactoe import TTTEnv, TTTGame, TTTNature, TTTPlayer


class TTTMonteCarloTestCase(TestCase,
                            MCTestCaseMixin[TTTEnv, TTTNature, TTTPlayer]):
    """TTTMonteCarloTestCase is the class for tic tac toe test cases."""

    @property
    def _test_count(self) -> int:
        return 10000

    def _create_game(self) -> TTTGame:
        return TTTGame()

    def _verify(self, game: SeqGame[TTTEnv, TTTNature, TTTPlayer]) -> None:
        super()._verify(game)

        assert game.env.winner is not None or not game.env.empty_coords


if __name__ == '__main__':
    main()
