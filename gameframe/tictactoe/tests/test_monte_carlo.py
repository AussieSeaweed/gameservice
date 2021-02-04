from random import choice
from typing import cast
from unittest import TestCase, main

from gameframe.sequential.tests.test_monte_carlo import MCTestCaseMixin
from gameframe.tictactoe import TTTGame, TTTPlayer


class TTTMCTestCase(TestCase, MCTestCaseMixin[TTTGame]):
    mc_test_count = 5000

    def verify(self, game: TTTGame) -> None:
        super().verify(game)

        if game.is_terminal:
            assert not game.env.empty_coords or game.env.winner is not None
        else:
            assert game.env.empty_coords and game.env.winner is None

    def act(self, game: TTTGame) -> None:
        cast(TTTPlayer, game.actor).mark(*choice([(r, c) for r, c in game.env.empty_coords]))

    def create_game(self) -> TTTGame:
        return TTTGame()


if __name__ == '__main__':
    main()
