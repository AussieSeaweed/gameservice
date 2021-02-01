from typing import Sequence
from unittest import TestCase, main

from gameframe.game import ActionException
from gameframe.tictactoe import TTTGame


class TTTSimTestCase(TestCase):
    def test_draws(self) -> None:
        games = [
            self.parse([1, 1], [0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]),
            self.parse([0, 0], [0, 2], [2, 0], [2, 2], [1, 2], [1, 0], [0, 1], [1, 1], [2, 1]),
            self.parse([0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [1, 1], [2, 0], [2, 2], [2, 1]),
            self.parse([0, 1], [0, 0], [1, 1], [0, 2], [1, 2], [1, 0], [2, 0], [2, 1], [2, 2]),
            self.parse([1, 1], [0, 2], [2, 2], [0, 0], [0, 1], [2, 1], [1, 0], [1, 2], [2, 0]),
        ]

        for game in games:
            self.assertIsNone(game.env.winner)

    def test_losses(self) -> None:
        games = [
            self.parse([2, 2], [0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0]),
            self.parse([1, 1], [0, 2], [1, 2], [1, 0], [2, 2], [0, 0], [0, 1], [2, 0]),
            self.parse([1, 1], [0, 1], [2, 0], [2, 2], [2, 1], [0, 2], [0, 0], [1, 2]),
            self.parse([0, 0], [1, 0], [0, 1], [1, 1], [2, 2], [1, 2]),
            self.parse([0, 1], [2, 0], [1, 1], [2, 1], [0, 2], [2, 2]),
        ]

        for game in games:
            self.assertEqual(game.players[1], game.env.winner)

    def test_wins(self) -> None:
        games = [
            self.parse([0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0]),
            self.parse([1, 1], [0, 2], [0, 1], [1, 2], [2, 1]),
            self.parse([1, 1], [0, 1], [2, 0], [0, 2], [0, 0], [1, 0], [2, 2]),
            self.parse([1, 1], [0, 1], [2, 0], [2, 2], [0, 2]),
            self.parse([0, 0], [1, 0], [0, 1], [1, 1], [0, 2]),
        ]

        for game in games:
            self.assertEqual(game.players[0], game.env.winner)

    def test_illegal_actions(self) -> None:
        self.assertRaises(ActionException, self.parse, [0, 0], [0, 0])
        self.assertRaises(ActionException, self.parse, [0, 0], [0, 1], [0, 0])
        self.assertRaises(ActionException, self.parse, [3, 3])
        self.assertRaises(ActionException, self.parse, [-1, -1])
        self.assertRaises(ActionException, self.parse, [2, 2], [2, 1], [2, 0], [1, 2], [1, 1], [1, 0], [0, 2], [0, 1])
        self.assertRaises(ActionException, self.parse([0, 0]).players[0].mark, 1, 1)

    @staticmethod
    def parse(*coords: Sequence[int]) -> TTTGame:
        game = TTTGame()

        for i, (r, c) in enumerate(coords):
            try:
                game.players[i % 2].mark(r, c)
            except ActionException as exception:
                assert i == len(coords) - 1, 'An exception was raised before all commands were parsed'
                raise exception

        return game


if __name__ == '__main__':
    main()
