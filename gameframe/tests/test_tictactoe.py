from random import choice
from typing import cast
from unittest import TestCase

from auxiliary import next_or_none

from gameframe.tests.utilities import MonteCarloTestCaseMixin
from gameframe.tictactoe import TicTacToe, TicTacToePlayer


class TicTacToeTest(MonteCarloTestCaseMixin[TicTacToe], TestCase):
    monte_carlo_test_count = 10000

    def create_game(self) -> TicTacToe:
        return TicTacToe()

    def act(self, game: TicTacToe) -> None:
        cast(TicTacToePlayer, game.actor).mark(*choice(tuple(game.empty_coords)))

    def verify(self, game: TicTacToe) -> None:
        if game.is_terminal():
            self.assertTrue(next_or_none(game.empty_coords) is None or game.winner is not None)
        else:
            self.assertFalse(next_or_none(game.empty_coords) is None or game.winner is not None)
