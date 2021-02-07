from random import choice
from typing import cast
from unittest import TestCase, main

from gameframe.sequential.tests.test_monte_carlo import SeqMCTestCaseMixin
from gameframe.tictactoe import TTTGame, TTTPlayer


class TTTMCTestCase(TestCase, SeqMCTestCaseMixin[TTTGame]):
    mc_test_count = 10000

    def verify(self, game: TTTGame) -> None:
        super().verify(game)

        if game.terminal:
            assert not game.empty_coords or game.winner is not None
        else:
            assert game.empty_coords and game.winner is None

    def act(self, game: TTTGame) -> None:
        cast(TTTPlayer, game.actor).mark(*choice([(r, c) for r, c in game.empty_coords]))

    def create_game(self) -> TTTGame:
        return TTTGame()


if __name__ == '__main__':
    main()
