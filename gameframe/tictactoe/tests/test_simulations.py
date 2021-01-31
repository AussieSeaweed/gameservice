from typing import Sequence
from unittest import TestCase, main

from gameframe.tictactoe import TTTGame


class TTTSimTestCase(TestCase):
    def test_draws(self) -> None:
        games = [
            self._sim([[1, 1], [0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]),
            self._sim([[0, 0], [0, 2], [2, 0], [2, 2], [1, 2], [1, 0], [0, 1], [1, 1], [2, 1]]),
            self._sim([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [1, 1], [2, 0], [2, 2], [2, 1]]),
            self._sim([[0, 1], [0, 0], [1, 1], [0, 2], [1, 2], [1, 0], [2, 0], [2, 1], [2, 2]]),
            self._sim([[1, 1], [0, 2], [2, 2], [0, 0], [0, 1], [2, 1], [1, 0], [1, 2], [2, 0]]),
        ]

        for game in games:
            self.assertIsNone(game.env.winner)

    def test_losses(self) -> None:
        games = [
            self._sim([[2, 2], [0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0]]),
            self._sim([[1, 1], [0, 2], [1, 2], [1, 0], [2, 2], [0, 0], [0, 1], [2, 0]]),
            self._sim([[1, 1], [0, 1], [2, 0], [2, 2], [2, 1], [0, 2], [0, 0], [1, 2]]),
            self._sim([[0, 0], [1, 0], [0, 1], [1, 1], [2, 2], [1, 2]]),
            self._sim([[0, 1], [2, 0], [1, 1], [2, 1], [0, 2], [2, 2]]),
        ]

        for game in games:
            self.assertEqual(game.players[1], game.env.winner)

    def test_wins(self) -> None:
        games = [
            self._sim([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0]]),
            self._sim([[1, 1], [0, 2], [0, 1], [1, 2], [2, 1]]),
            self._sim([[1, 1], [0, 1], [2, 0], [0, 2], [0, 0], [1, 0], [2, 2]]),
            self._sim([[1, 1], [0, 1], [2, 0], [2, 2], [0, 2]]),
            self._sim([[0, 0], [1, 0], [0, 1], [1, 1], [0, 2]]),
        ]

        for game in games:
            self.assertEqual(game.players[0], game.env.winner)

    def test_illegal_actions(self) -> None:
        self.assertRaises(ValueError, self._sim, [[0, 0], [0, 0]])
        self.assertRaises(ValueError, self._sim, [[0, 0], [0, 1], [0, 0]])
        self.assertRaises(ValueError, self._sim, [[3, 3]])
        self.assertRaises(ValueError, self._sim, [[-1, -1]])
        self.assertRaises(ValueError, self._sim, [[2, 2], [2, 1], [2, 0], [1, 2], [1, 1], [1, 0], [0, 2], [0, 1]])
        self.assertRaises(ValueError, self._sim([[0, 0]]).players[0].mark, 1, 1)

    @staticmethod
    def _sim(coords: Sequence[Sequence[int]]) -> TTTGame:
        game = TTTGame()

        for i, (r, c) in enumerate(coords):
            game.players[i % 2].mark(r, c)

        return game


if __name__ == '__main__':
    main()
