from abc import ABC
from random import randint
from unittest import TestCase, main

from gameframe.poker import NoLimitGreekHoldEmGame, NoLimitOmahaHoldEmGame, NoLimitTexasHoldEmGame, PokerGame
from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin


def starting_stacks_factory():
    return [randint(0, 100) for _ in range(randint(2, 6))]


ante = 1
blinds = [1, 2]
lazy = True


class PokerMonteCarloTestCaseMixin(SequentialMonteCarloTestCaseMixin, ABC):
    """PokerMonteCarloTestCaseMixin is the mixin for all poker monte carlo test cases."""

    @property
    def _test_count(self):
        return 1000

    def _verify(self, game):
        assert sum(game.starting_stacks) == sum(player.stack for player in game.players)
        assert all(player.stack >= 0 and player.bet == 0 for player in game.players)
        assert game.environment.pot == 0


class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitTexasHoldEmMonteCarloTestCase is the class for no-limit texas hold'em test cases."""

    def _create_game(self):
        return NoLimitTexasHoldEmGame(ante, blinds, starting_stacks_factory(), lazy)


class NoLimitGreekHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitGreekHoldEmMonteCarloTestCase is the class for no-limit greek hold'em test cases."""

    def _create_game(self):
        return NoLimitGreekHoldEmGame(ante, blinds, starting_stacks_factory(), lazy)


class NoLimitOmahaHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitOmahaHoldEmMonteCarloTestCase is the class for no-limit omaha hold'em test cases."""

    def _create_game(self):
        return NoLimitOmahaHoldEmGame(ante, blinds, starting_stacks_factory(), lazy)


if __name__ == '__main__':
    main()
