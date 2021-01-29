from abc import ABC
from random import randint
from unittest import TestCase, main

from gameframe.poker import (NLGreekHEGame, NLOmahaHEGame, NLTexasHEGame,
                             PokerEnv, PokerNature, PokerPlayer)
from gameframe.sequential.tests import MCTestCaseMixin


def create_stacks():
    return [randint(0, 100) for _ in range(randint(2, 6))]


ante = 1
blinds = [1, 2]
laziness = True


class PokerMCTestCaseMixin(MCTestCaseMixin[PokerEnv, PokerNature, PokerPlayer],
                           ABC):
    """PokerMCTestCaseMixin is the mixin for all poker monte carlo test cases.
    """

    @property
    def _test_count(self) -> int:
        return 1000

    def _verify(self, game) -> None:
        super()._verify(game)

        if game.is_terminal:
            assert all(player.bet == 0 for player in game.players)
            assert sum(player.stack for player in game.players) \
                   == sum(game.starting_stacks)
            assert sum(player.payoff for player in game.players) == 0
            assert game.env.pot == 0


class NLGreekHEMCTestCase(TestCase, PokerMCTestCaseMixin):
    """NLGreekHEMCTestCase is the class for no-limit texas hold'em test cases.
    """

    def _create_game(self) -> NLGreekHEGame:
        return NLGreekHEGame(ante, blinds, create_stacks(), laziness)


class NLOmahaHEMCTestCase(TestCase, PokerMCTestCaseMixin):
    """NLOmahaHEMCTestCase is the class for no-limit greek hold'em test cases.
    """

    def _create_game(self) -> NLOmahaHEGame:
        return NLOmahaHEGame(ante, blinds, create_stacks(), laziness)


class NLTexasHEMCTestCase(TestCase, PokerMCTestCaseMixin):
    """NLTexasHEMCTestCase is the class for no-limit omaha hold'em test cases.
    """

    def _create_game(self) -> NLTexasHEGame:
        return NLTexasHEGame(ante, blinds, create_stacks(), laziness)


if __name__ == '__main__':
    main()
