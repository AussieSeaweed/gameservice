from abc import ABC, abstractmethod
from random import choice, randint, sample
from typing import Generic, cast
from unittest import TestCase, main

from auxiliary import next_or_none

from gameframe.game import _G
from gameframe.poker import NLTGame, PokerNature, PokerPlayer, parse_poker
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


class NoLimitTexasHoldEmTestCase(TestCase, MonteCarloTestCaseMixin[NLTGame]):
    MONTE_CARLO_TEST_COUNT = 1000

    ANTE = 1
    BLINDS = 1, 2
    PLAYER_COUNT = 6
    MIN_STACK = 0
    MAX_STACK = 20

    def verify(self, game: NLTGame) -> None:
        super().verify(game)

        if game.terminal:
            self.assertEqual(game.pot, 0)
            self.assertTrue(all(player.bet == 0 and player.stack >= 0 for player in game.players))

        self.assertEqual(game.pot + sum(player.bet + player.stack for player in game.players),
                         sum(player.starting_stack for player in game.players))

    def act(self, game: NLTGame) -> None:
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

    def create_game(self) -> NLTGame:
        return NLTGame(
            self.ANTE, self.BLINDS, (randint(self.MIN_STACK, self.MAX_STACK) for _ in range(self.PLAYER_COUNT)),
        )


class TicTacToeMonteCarloTestCase(TestCase, MonteCarloTestCaseMixin[TicTacToe]):
    MONTE_CARLO_TEST_COUNT = 10000

    def create_game(self) -> TicTacToe:
        return TicTacToe()

    def act(self, game: TicTacToe) -> None:
        cast(TicTacToePlayer, game.actor).mark(*choice(tuple(game.empty_coords)))

    def verify(self, game: TicTacToe) -> None:
        if game.terminal:
            self.assertTrue(next_or_none(game.empty_coords) is None or game.winner is not None)
        else:
            self.assertTrue(next_or_none(game.empty_coords) is not None and game.winner is None)


class RockPaperScissorsMonteCarloTestCase(TestCase, MonteCarloTestCaseMixin[RockPaperScissors]):
    MONTE_CARLO_TEST_COUNT = 100000

    def create_game(self) -> RockPaperScissors:
        return RockPaperScissors()

    def act(self, game: RockPaperScissors) -> None:
        for player in game.players:
            player.throw(choice(tuple(RockPaperScissorsHand)))

    def verify(self, game: RockPaperScissors) -> None:
        if game.terminal:
            if game.winner is game.players[0]:
                self.assertGreater(game.players[0].hand, game.players[1].hand)
            elif game.winner is game.players[1]:
                self.assertLess(game.players[0].hand, game.players[1].hand)
            else:
                self.assertEqual(game.players[0].hand, game.players[1].hand)


if __name__ == '__main__':
    main()
