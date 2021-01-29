from abc import ABC, abstractmethod
from random import choice

from gameframe.game import Env, Nature, Player
from gameframe.sequential import SequentialGame


class MonteCarloTestCaseMixin(ABC):
    """MonteCarloTestCaseMixin is the abstract base mixin for all monte carlo
    test cases.
    """

    @property
    @abstractmethod
    def _test_count(self) -> int:
        pass

    @abstractmethod
    def test_monte_carlo(self) -> None:
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any
        tests
        """
        for i in range(self._test_count):
            game = self._create_game()

            while not game.is_terminal:
                choice(game.actor.actions).act()

            self._verify(game)

    @abstractmethod
    def _create_game(self) -> SequentialGame[Env, Nature, Player]:
        pass

    @abstractmethod
    def _verify(self, game: SequentialGame[Env, Nature, Player]) -> None:
        pass
