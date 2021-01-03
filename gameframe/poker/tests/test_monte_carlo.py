from abc import ABC
from random import randint
from typing import Callable, List, final
from unittest import TestCase, main

from gameframe.poker import NoLimitGreekHoldEmGame, NoLimitOmahaHoldEmGame, NoLimitTexasHoldEmGame, PokerGame
from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin
from gameframe.utils import override

ante: int = 1
blinds: List[int] = [1, 2]
starting_stacks_factory: Callable[[], List[int]] = lambda: [randint(0, 100) for _ in range(randint(2, 6))]
lazy = True


class PokerMonteCarloTestCaseMixin(SequentialMonteCarloTestCaseMixin[PokerGame], ABC):
    """PokerMonteCarloTestCaseMixin is the mixin for all poker monte carlo test cases."""

    _test_count: int = 1000

    @override
    def _verify_game(self, game: NoLimitTexasHoldEmGame) -> None:
        assert sum(game._starting_stacks) == sum(player.stack for player in game.players)
        assert all(player.stack >= 0 and player.bet == 0 for player in game.players)
        assert game.environment.pot == 0


@final
class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitTexasHoldEmMonteCarloTestCase is the class for no-limit texas hold'em test cases."""

    @override
    def _create_game(self) -> NoLimitTexasHoldEmGame:
        return NoLimitTexasHoldEmGame(ante, blinds, starting_stacks_factory(), lazy)


@final
class NoLimitGreekHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitGreekHoldEmMonteCarloTestCase is the class for no-limit greek hold'em test cases."""

    @override
    def _create_game(self) -> NoLimitGreekHoldEmGame:
        return NoLimitGreekHoldEmGame(ante, blinds, starting_stacks_factory(), lazy)


@final
class NoLimitOmahaHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitOmahaHoldEmMonteCarloTestCase is the class for no-limit omaha hold'em test cases."""

    @override
    def _create_game(self) -> NoLimitOmahaHoldEmGame:
        return NoLimitOmahaHoldEmGame(ante, blinds, starting_stacks_factory(), lazy)


if __name__ == '__main__':
    main()