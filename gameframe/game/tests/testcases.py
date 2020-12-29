from abc import ABC, abstractmethod


class GameTestCaseMixin(ABC):
    """GameTestCaseMixin is the abstract base mixin for all game test cases."""

    @abstractmethod
    def test_monte_carlo(self):
        """Runs monte carlo tests of games.

        :return: None
        :raise AssertionError: if the game integrity verification fails in any tests
        """
        pass

    @abstractmethod
    def _create_game(self):
        pass

    @abstractmethod
    def _verify(self, game):
        pass

    @property
    @abstractmethod
    def _num_monte_carlo_tests(self):
        pass
