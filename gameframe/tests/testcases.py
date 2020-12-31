from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice
from typing import Generic
from unittest import TestCase, main

from gameframe.game import G
from gameframe.sequential import SG
from gameframe.tictactoe import TicTacToeGame


class GameTestCaseMixin(Generic[G], ABC):
    """GameTestCaseMixin is the abstract base mixin for all game test cases."""

    @abstractmethod
    def test_monte_carlo(self: GameTestCaseMixin[G]) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        pass

    @abstractmethod
    def _create_game(self: GameTestCaseMixin[G]) -> G:
        pass

    @abstractmethod
    def _verify(self: GameTestCaseMixin[G], game: G) -> None:
        pass

    @property
    @abstractmethod
    def _num_monte_carlo_tests(self: GameTestCaseMixin[G]) -> int:
        pass


class SequentialTestCaseMixin(GameTestCaseMixin[SG], Generic[SG], ABC):
    """SequentialTestCaseMixin is the abstract base mixin for all sequential test cases."""

    def test_monte_carlo(self: SequentialTestCaseMixin[SG]) -> None:
        for i in range(self._num_monte_carlo_tests):
            game: SG = self._create_game()

            while not game.terminal:
                choice(game.actor.actions).act()

            self._verify(game)


class TicTacToeTestCase(TestCase, SequentialTestCaseMixin[TicTacToeGame]):
    """TicTacToeTestCase is the class for tic tac toe test cases."""

    def test_draw(self: TicTacToeTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[4].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([0, 0], [player.payoff for player in game.players])

    def test_loss(self: TicTacToeTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of the first player losing.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[8].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([-1, 1], [player.payoff for player in game.players])

    def test_win(self: TicTacToeTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([1, -1], [player.payoff for player in game.players])

    def _create_game(self: TicTacToeTestCase) -> TicTacToeGame:
        return TicTacToeGame()

    def _verify(self: TicTacToeTestCase, game: TicTacToeGame) -> None:
        assert game.environment._winner is not None or not game.environment._empty_coordinates

    @property
    def _num_monte_carlo_tests(self: TicTacToeTestCase) -> int:
        return 10000


if __name__ == '__main__':
    main()
