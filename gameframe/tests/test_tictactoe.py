from random import choice
from typing import cast
from unittest import TestCase, main

from auxiliary import next_or_none

from gameframe.exceptions import GameFrameError
from gameframe.tests import GameFrameTestCaseMixin
from gameframe.tictactoe import TicTacToe, TicTacToePlayer, parse_tic_tac_toe


class TicTacToeTest(GameFrameTestCaseMixin[TicTacToe], TestCase):
    MONTE_CARLO_TEST_COUNT = 1000
    SPEED_TEST_TIME = 1

    def test_draws(self) -> None:
        for game in (
                parse_tic_tac_toe(
                    TicTacToe(),
                    ((1, 1), (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)),
                ),
                parse_tic_tac_toe(
                    TicTacToe(),
                    ((0, 0), (0, 2), (2, 0), (2, 2), (1, 2), (1, 0), (0, 1), (1, 1), (2, 1)),
                ),
                parse_tic_tac_toe(
                    TicTacToe(),
                    ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)),
                ),
                parse_tic_tac_toe(
                    TicTacToe(),
                    ((0, 1), (0, 0), (1, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1), (2, 2)),
                ),
                parse_tic_tac_toe(
                    TicTacToe(),
                    ((1, 1), (0, 2), (2, 2), (0, 0), (0, 1), (2, 1), (1, 0), (1, 2), (2, 0)),
                ),
        ):
            self.assertIsNone(game.winner)

    def test_losses(self) -> None:
        for game in (
                parse_tic_tac_toe(TicTacToe(), ((2, 2), (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0))),
                parse_tic_tac_toe(TicTacToe(), ((1, 1), (0, 2), (1, 2), (1, 0), (2, 2), (0, 0), (0, 1), (2, 0))),
                parse_tic_tac_toe(TicTacToe(), ((1, 1), (0, 1), (2, 0), (2, 2), (2, 1), (0, 2), (0, 0), (1, 2))),
                parse_tic_tac_toe(TicTacToe(), ((0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (1, 2))),
                parse_tic_tac_toe(TicTacToe(), ((0, 1), (2, 0), (1, 1), (2, 1), (0, 2), (2, 2))),
        ):
            self.assertIs(game.players[1], game.winner)

    def test_wins(self) -> None:
        for game in (
                parse_tic_tac_toe(TicTacToe(), ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0))),
                parse_tic_tac_toe(TicTacToe(), ((1, 1), (0, 2), (0, 1), (1, 2), (2, 1))),
                parse_tic_tac_toe(TicTacToe(), ((1, 1), (0, 1), (2, 0), (0, 2), (0, 0), (1, 0), (2, 2))),
                parse_tic_tac_toe(TicTacToe(), ((1, 1), (0, 1), (2, 0), (2, 2), (0, 2))),
                parse_tic_tac_toe(TicTacToe(), ((0, 0), (1, 0), (0, 1), (1, 1), (0, 2))),
        ):
            self.assertIs(game.players[0], game.winner)

    def test_illegal_actions(self) -> None:
        self.assertRaises(GameFrameError, parse_tic_tac_toe, parse_tic_tac_toe(TicTacToe(), ((0, 0),)), ((0, 0),))
        self.assertRaises(
            GameFrameError,
            parse_tic_tac_toe,
            parse_tic_tac_toe(TicTacToe(), ((0, 0), (0, 1))),
            ((0, 0),),
        )
        self.assertRaises(GameFrameError, parse_tic_tac_toe, TicTacToe(), ((3, 3),))
        self.assertRaises(GameFrameError, parse_tic_tac_toe, TicTacToe(), ((-1, -1),))
        self.assertRaises(GameFrameError, parse_tic_tac_toe(TicTacToe(), ((0, 0),)).players[0].mark, 0, 1)

    def create_game(self) -> TicTacToe:
        return TicTacToe()

    def act(self, game: TicTacToe) -> None:
        cast(TicTacToePlayer, game.actor).mark(*choice(tuple(game.empty_coordinates)))

    def verify(self, game: TicTacToe) -> None:
        if game.terminal:
            self.assertTrue(next_or_none(game.empty_coordinates) is None or game.winner is not None)

            self.assertFalse(game.players[0].can_mark())
            self.assertFalse(game.players[1].can_mark())

            for r in range(3):
                for c in range(3):
                    self.assertFalse(game.players[0].can_mark(r, c))
                    self.assertFalse(game.players[1].can_mark(r, c))
        else:
            self.assertFalse(next_or_none(game.empty_coordinates) is None or game.winner is not None)

            actor = cast(TicTacToePlayer, game.actor)
            non_actor = game.players[1 if game.players[0] is actor else 0]

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
