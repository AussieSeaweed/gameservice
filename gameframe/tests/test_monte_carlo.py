from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice
from typing import Generic
from unittest import TestCase, main

from gameframe.game import G
from gameframe.sequential import SG
from gameframe.tictactoe import TicTacToeGame


class MonteCarloTestCaseMixin(Generic[G], ABC):
    """MonteCarloTestCaseMixin is the abstract base mixin for all monte carlo test cases."""

    @abstractmethod
    def test_monte_carlo(self: MonteCarloTestCaseMixin[G]) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        pass

    @abstractmethod
    def _create_game(self: MonteCarloTestCaseMixin[G]) -> G:
        pass

    @abstractmethod
    def _verify(self: MonteCarloTestCaseMixin[G], game: G) -> None:
        pass

    @property
    @abstractmethod
    def _num_monte_carlo_tests(self: MonteCarloTestCaseMixin[G]) -> int:
        pass


class SequentialMonteCarloTestCaseMixin(MonteCarloTestCaseMixin[SG], Generic[SG], ABC):
    """SequentialMonteCarloTestCaseMixin is the abstract base mixin for all sequential monte carlo test cases."""

    def test_monte_carlo(self: SequentialMonteCarloTestCaseMixin[SG]) -> None:
        for i in range(self._num_monte_carlo_tests):
            game: SG = self._create_game()

            while not game.terminal:
                choice(game.actor.actions).act()

            self._verify(game)


class TicTacToeMonteCarloTestCase(TestCase, SequentialMonteCarloTestCaseMixin[TicTacToeGame]):
    """TicTacToeTestCase is the class for tic tac toe test cases."""

    def test_draw(self: TicTacToeMonteCarloTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[4].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([0, 0], [player.payoff for player in game.players])

    def test_loss(self: TicTacToeMonteCarloTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of the first player losing.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        game.actor.actions[8].act()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([-1, 1], [player.payoff for player in game.players])

    def test_win(self: TicTacToeMonteCarloTestCase) -> None:
        """Tests if the tic tac toe properly detects a case of the first player winning.

        :return: None
        :raise AssertionError: if the tic tac toe player payoffs are wrong
        """
        game: TicTacToeGame = self._create_game()

        while not game.terminal:
            game.actor.actions[0].act()

        self.assertEqual([1, -1], [player.payoff for player in game.players])

    def _create_game(self: TicTacToeMonteCarloTestCase) -> TicTacToeGame:
        return TicTacToeGame()

    def _verify(self: TicTacToeMonteCarloTestCase, game: TicTacToeGame) -> None:
        assert game.environment._winner is not None or not game.environment._empty_coordinates

    @property
    def _num_monte_carlo_tests(self: TicTacToeMonteCarloTestCase) -> int:
        return 10000


if __name__ == '__main__':
    main()
