from random import choice
from typing import cast
from unittest import TestCase, main

from gameframe.sequential.tests.test_monte_carlo import MCTestCaseMixin
from gameframe.tictactoe import TTTGame
from gameframe.tictactoe.bases import MarkAction, TTTPlayer


class TTTMCTestCase(TestCase, MCTestCaseMixin[TTTGame]):
    @property
    def test_count(self) -> int:
        return 2000

    def verify(self, game: TTTGame) -> None:
        super().verify(game)

        if game.is_terminal:
            assert game.env.winner is not None or not game.env.empty_coords
        else:
            assert game.env.winner is None and game.env.empty_coords

    def act(self, game: TTTGame) -> None:
        choice([MarkAction(game, cast(TTTPlayer, game.env.actor), r, c) for r, c in game.env.empty_coords]).act()

    def create_game(self) -> TTTGame:
        return TTTGame()


if __name__ == '__main__':
    main()
