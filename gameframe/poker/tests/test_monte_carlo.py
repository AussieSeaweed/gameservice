from abc import ABC
from random import randint
from unittest import TestCase, main

from gameframe.poker import NoLimitTexasHoldEmGame
from gameframe.sequential.tests import SequentialMonteCarloTestCaseMixin


def starting_stacks_factory():
    return [randint(0, 1000) for _ in range(randint(2, 6))]


ante = 1
blinds = [1, 2]
laziness = True


class PokerMonteCarloTestCaseMixin(SequentialMonteCarloTestCaseMixin, ABC):
    """PokerMonteCarloTestCaseMixin is the mixin for all poker monte carlo test cases."""

    @property
    def _test_count(self):
        return 1000

    def _verify(self, game):
        assert all(player.bet == 0 for player in game.players)
        assert sum(player.stack for player in game.players) == sum(game.starting_stacks)
        assert sum(player.payoff for player in game.players) == 0
        assert game.environment.pot == 0


class NoLimitTexasHoldEmMonteCarloTestCase(TestCase, PokerMonteCarloTestCaseMixin):
    """NoLimitTexasHoldEmMonteCarloTestCase is the class for no-limit texas hold'em test cases."""

    def _create_game(self):
        return NoLimitTexasHoldEmGame(ante, blinds, starting_stacks_factory(), laziness)


if __name__ == '__main__':
    main()
