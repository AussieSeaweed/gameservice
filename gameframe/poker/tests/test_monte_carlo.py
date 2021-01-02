from unittest import TestCase, main
from typing import final, Sequence

from gameframe.poker import NoLimitTexasHoldEmGame
from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin


class CustomNoLimitTexasHoldEmGame(NoLimitTexasHoldEmGame):
    """CustomNoLimitTexasHoldEmGame is the class for custom no-limit texas hold'em games."""

    @property
    def small_blind(self) -> int:
        return 1

    @property
    def big_blind(self) -> int:
        return 2

    @property
    def ante(self) -> int:
        return 0

    @property
    def starting_stacks(self) -> Sequence[int]:
        return [100, 200, 300, 200, 300, 100]

    @property
    def _lazy(self) -> bool:
        return True


class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, SequentialMonteCarloTestCaseMixin[CustomNoLimitTexasHoldEmGame]):
    """NoLimitTexasHoldEmMonteCarloTestCase is the class for custom no-limit texas hold'em test cases."""

    @property
    def _monte_carlo_test_count(self) -> int:
        return 1000

    def _create_game(self) -> CustomNoLimitTexasHoldEmGame:
        return CustomNoLimitTexasHoldEmGame()

    def _verify_game(self, game: CustomNoLimitTexasHoldEmGame) -> None:
        assert sum(game.starting_stacks) == sum(player.stack for player in game.players) \
               and all(player.stack >= 0 and player.bet >= 0 for player in game.players)


if __name__ == '__main__':
    main()
