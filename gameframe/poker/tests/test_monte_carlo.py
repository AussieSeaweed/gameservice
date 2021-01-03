from abc import ABC
from typing import final
from unittest import TestCase, main
from random import randint

from gameframe.poker import NoLimitTexasHoldEmGame, PokerGame, FixedLimitTexasHoldEmGame, NoLimitOmahaHoldEmGame, FixedLimitOmahaHoldEmGame, NoLimitGreekHoldEmGame, FixedLimitGreekHoldEmGame
from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin
from gameframe.utils import override


class PokerMonteCarloTestCaseMixin(SequentialMonteCarloTestCaseMixin[PokerGame], ABC):
    """PokerMonteCarloTestCaseMixin is the mixin for all poker monte carlo test cases."""

    _test_count: int = 1000

    @override
    def _verify_game(self, game: NoLimitTexasHoldEmGame) -> None:
        assert sum(game._starting_stacks) == sum(player.stack for player in game.players)
        assert all(player.stack >= 0 and player.bet == 0 for player in game.players)


@final
class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitTexasHoldEmMonteCarloTestCase is the class for no-limit texas hold'em test cases."""

    @override
    def _create_game(self) -> NoLimitTexasHoldEmGame:
        return NoLimitTexasHoldEmGame(1, [1, 2], [randint(0, 10) for _ in range(6)], True)


@final
class FixedLimitTexasHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """FixedLimitTexasHoldEmMonteCarloTestCase is the class for fixed-limit texas hold'em test cases."""

    @override
    def _create_game(self) -> FixedLimitTexasHoldEmGame:
        return FixedLimitTexasHoldEmGame(1, [1, 2], [randint(0, 10) for _ in range(6)], True)


@final
class NoLimitGreekHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitGreekHoldEmMonteCarloTestCase is the class for no-limit greek hold'em test cases."""

    @override
    def _create_game(self) -> NoLimitGreekHoldEmGame:
        return NoLimitGreekHoldEmGame(1, [1, 2], [randint(0, 10) for _ in range(6)], True)


@final
class FixedLimitGreekHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """FixedLimitGreekHoldEmMonteCarloTestCase is the class for limit greek hold'em test cases."""

    @override
    def _create_game(self) -> FixedLimitGreekHoldEmGame:
        return FixedLimitGreekHoldEmGame(1, [1, 2], [randint(0, 10) for _ in range(6)], True)


@final
class NoLimitOmahaHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitOmahaHoldEmMonteCarloTestCase is the class for no-limit omaha hold'em test cases."""

    @override
    def _create_game(self) -> NoLimitOmahaHoldEmGame:
        return NoLimitOmahaHoldEmGame(1, [1, 2], [randint(0, 10) for _ in range(6)], True)


@final
class FixedLimitOmahaHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """FixedLimitOmahaHoldEmMonteCarloTestCase is the class for limit omaha hold'em test cases."""

    @override
    def _create_game(self) -> FixedLimitOmahaHoldEmGame:
        return FixedLimitOmahaHoldEmGame(1, [1, 2], [randint(0, 10) for _ in range(6)], True)



if __name__ == '__main__':
    main()
