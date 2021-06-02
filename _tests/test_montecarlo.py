from abc import ABC, abstractmethod
from random import choice, randint, sample
from typing import Generic, cast
from unittest import TestCase, main

from auxiliary import next_or_none

from gameframe.game import _G
from gameframe.poker import NoLimitTexasHoldEm, PokerNature, PokerPlayer, parse_poker
from gameframe.rockpaperscissors import RockPaperScissors, RockPaperScissorsHand
from gameframe.tictactoe import TicTacToe, TicTacToePlayer


class MonteCarloTestCaseMixin(Generic[_G], ABC):
    MONTE_CARLO_TEST_COUNT: int

    def test_monte_carlo(self) -> None:
        for i in range(self.MONTE_CARLO_TEST_COUNT):
            game = self.create_game()

            self.verify(game)

            while not game.terminal:
                self.act(game)
                self.verify(game)

    @abstractmethod
    def create_game(self) -> _G:
        pass

    @abstractmethod
    def act(self, game: _G) -> None:
        pass

    @abstractmethod
    def verify(self, game: _G) -> None:
        pass


class NoLimitTexasHoldEmTestCase(TestCase, MonteCarloTestCaseMixin[NoLimitTexasHoldEm]):
    MONTE_CARLO_TEST_COUNT = 1000

    ANTE = 1
    BLINDS = 1, 2
    MIN_PLAYER_COUNT = 2
    MAX_PLAYER_COUNT = 9
    MIN_STACK = 0
    MAX_STACK = 20

    def verify(self, game: NoLimitTexasHoldEm) -> None:
        super().verify(game)

        if game.terminal:
            self.assertEqual(game.pot, 0)
            self.assertTrue(all(player.bet == 0 and player.stack >= 0 for player in game.players))

        self.assertEqual(game.pot + sum(player.bet + player.stack for player in game.players),
                         sum(player.starting_stack for player in game.players))

    def act(self, game: NoLimitTexasHoldEm) -> None:
        if isinstance(game.actor, PokerNature):
            if game.actor.can_deal_hole():
                for player in game.players:
                    game.nature.deal_hole(player, sample(tuple(game.deck), game.actor.hole_deal_count))
            elif game.actor.can_deal_board():
                game.nature.deal_board(sample(tuple(game.deck), game.actor.board_deal_count))
            else:
                self.fail()
        elif isinstance(game.actor, PokerPlayer):
            actions = []

            if game.actor.can_fold():
                actions.append('f')

            if game.actor.can_check_call():
                actions.append('cc')

            if game.actor.can_bet_raise():
                actions.extend({f'br {game.actor.min_bet_raise}', f'br {game.actor.max_bet_raise}'})

            if game.actor.can_showdown():
                actions.extend(('s 0', 's 1'))

            parse_poker(game, (choice(actions),))

    def create_game(self) -> NoLimitTexasHoldEm:
        return NoLimitTexasHoldEm(
            self.ANTE, self.BLINDS, tuple(randint(self.MIN_STACK, self.MAX_STACK) for _ in range(randint(
                self.MIN_PLAYER_COUNT, self.MAX_PLAYER_COUNT))),
        )


if __name__ == '__main__':
    main()
