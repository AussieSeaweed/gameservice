from abc import ABC, abstractmethod


class MonteCarloTestCaseMixin(ABC):
    """MonteCarloTestCaseMixin is the abstract base mixin for all monte carlo test cases."""

    @property
    @abstractmethod
    def _test_count(self):
        pass

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
