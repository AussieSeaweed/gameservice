from typing import final
from unittest import TestCase, main
from random import randint

from gameframe.poker import NoLimitTexasHoldEmGame
from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin
from gameframe.utils import override


@final
class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, SequentialMonteCarloTestCaseMixin[NoLimitTexasHoldEmGame]):
    """NoLimitTexasHoldEmMonteCarloTestCase is the class for custom no-limit texas hold'em test cases."""

    _test_count: int = 1000

    @override
    def _create_game(self) -> NoLimitTexasHoldEmGame:
        return NoLimitTexasHoldEmGame(1, [1, 2], [randint(0, 100) for _ in range(6)], True)

    @override
    def _verify_game(self, game: NoLimitTexasHoldEmGame) -> None:
        assert sum(game._starting_stacks) == sum(player.stack for player in game.players) \
               and all(player.stack >= 0 and player.bet >= 0 for player in game.players)


if __name__ == '__main__':
    main()
