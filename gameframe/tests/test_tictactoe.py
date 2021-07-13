from unittest import TestCase, main

from auxiliary import next_or_none

from gameframe.exceptions import GameFrameError
from gameframe.games.tictactoe import TicTacToeGame
from gameframe.tests import GameFrameTestCaseMixin


class TicTacToeTestCase(GameFrameTestCaseMixin, TestCase):
    def test_draws(self):
        for game in (
                TicTacToeGame().mark((1, 1), (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)),
                TicTacToeGame().mark((0, 0), (0, 2), (2, 0), (2, 2), (1, 2), (1, 0), (0, 1), (1, 1), (2, 1)),
                TicTacToeGame().mark((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)),
                TicTacToeGame().mark((0, 1), (0, 0), (1, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1), (2, 2)),
                TicTacToeGame().mark((1, 1), (0, 2), (2, 2), (0, 0), (0, 1), (2, 1), (1, 0), (1, 2), (2, 0)),
        ):
            self.assertIsNone(game.winner)

    def test_losses(self):
        for game in (
                TicTacToeGame().mark((2, 2), (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0)),
                TicTacToeGame().mark((1, 1), (0, 2), (1, 2), (1, 0), (2, 2), (0, 0), (0, 1), (2, 0)),
                TicTacToeGame().mark((1, 1), (0, 1), (2, 0), (2, 2), (2, 1), (0, 2), (0, 0), (1, 2)),
                TicTacToeGame().mark((0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2)),
                TicTacToeGame().mark((0, 1), (2, 0), (1, 1), (2, 1), (0, 2), (2, 2)),
        ):
            self.assertIs(game.players[1], game.winner)

    def test_wins(self):
        for game in (
                TicTacToeGame().mark((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0)),
                TicTacToeGame().mark((1, 1), (0, 2), (0, 1), (1, 2), (2, 1)),
                TicTacToeGame().mark((1, 1), (0, 1), (2, 0), (0, 2), (0, 0), (1, 0), (2, 2)),
                TicTacToeGame().mark((1, 1), (0, 1), (2, 0), (2, 2), (0, 2)),
                TicTacToeGame().mark((0, 0), (1, 0), (0, 1), (1, 1), (0, 2)),
        ):
            self.assertIs(game.players[0], game.winner)

    def test_illegal_actions(self):
        self.assertRaises(GameFrameError, TicTacToeGame().mark((0, 0)).mark, (0, 0))
        self.assertRaises(GameFrameError, TicTacToeGame().mark((0, 0), (0, 1)).mark, (0, 0))
        self.assertRaises(GameFrameError, TicTacToeGame().mark, (3, 3))
        self.assertRaises(GameFrameError, TicTacToeGame().mark, (-1, -1))
        self.assertRaises(GameFrameError, TicTacToeGame().mark((0, 0)).players[0].mark, 0, 1)

    def create_game(self):
        return TicTacToeGame()

    def act(self, game):
        game.actor.mark()

    def verify(self, game):
        if game.is_terminal():
            self.assertTrue(next_or_none(game.empty_coordinates) is None or game.winner is not None)

            self.assertFalse(game.players[0].can_mark())
            self.assertFalse(game.players[1].can_mark())

            for r in range(3):
                for c in range(3):
                    self.assertFalse(game.players[0].can_mark(r, c))
                    self.assertFalse(game.players[1].can_mark(r, c))
        else:
            self.assertFalse(next_or_none(game.empty_coordinates) is None or game.winner is not None)

            actor = game.actor
            non_actor = next(actor)

            self.assertTrue(actor.can_mark())
            self.assertFalse(non_actor.can_mark())

            for r in range(3):
                for c in range(3):
                    if game.board[r][c] is None:
                        self.assertTrue(actor.can_mark(r, c))
                    else:
                        self.assertFalse(actor.can_mark(r, c))

                    self.assertFalse(non_actor.can_mark(r, c))


if __name__ == '__main__':
    main()
