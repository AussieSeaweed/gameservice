from random import choice
from unittest import TestCase, main

from gameframe.sequential.tests.test_monte_carlo import SeqMCTestCaseMixin
from gameframe.tictactoe import TTTGame


class TTTMCTestCase(TestCase, SeqMCTestCaseMixin[TTTGame]):
    MC_TEST_COUNT = 10000

    def verify(self, game: TTTGame) -> None:
        super().verify(game)

        if game.terminal:
            assert not game.empty_coords or game.winner is not None
        else:
            assert game.empty_coords and game.winner is None

    def act(self, game: TTTGame) -> None:
        assert game.actor is not None
        game.actor.mark(*choice([(r, c) for r, c in game.empty_coords]))

    def create_game(self) -> TTTGame:
        return TTTGame()


if __name__ == '__main__':
    main()
