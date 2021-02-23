from random import choice, randint, sample
from typing import cast
from unittest import TestCase, main

from gameframe.poker import NLTGame, PokerPlayer, parse_poker_game
from gameframe.poker._stages import BettingStage, BoardCardDealingStage, HoleCardDealingStage, ShowdownStage
from gameframe.sequential.tests.test_monte_carlo import SeqMCTestCaseMixin


class NLTMCTestCase(TestCase, SeqMCTestCaseMixin[NLTGame]):
    ANTE = 1
    BLINDS = [1, 2]
    PLAYER_COUNT = 6
    MIN_STACK = 0
    MAX_STACK = 20

    MC_TEST_COUNT = 1000

    def verify(self, game: NLTGame) -> None:
        super().verify(game)

        if game.terminal:
            self.assertEqual(game.pot, 0)
            self.assertTrue(all(player.bet == 0 and player.stack >= 0 for player in game.players))

        self.assertEqual(game.pot + sum(player.bet + player.stack for player in game.players),
                         sum(player.starting_stack for player in game.players))

    def act(self, game: NLTGame) -> None:
        if isinstance(game._stage, HoleCardDealingStage):
            for player in game.players:
                game.nature.deal_player(player, sample(game.deck, game._stage.card_count))
        if isinstance(game._stage, BoardCardDealingStage):
            game.nature.deal_board(sample(game.deck, game._stage.card_count))
        elif isinstance(game._stage, BettingStage):
            actor = cast(PokerPlayer, game.actor)
            actions = []

            if actor.can_fold():
                actions.append('f')

            if actor.can_check_call():
                actions.append('cc')

            if actor.can_bet_raise():
                actions.extend({f'br {actor.min_bet_raise_amount}', f'br {actor.max_bet_raise_amount}'})

            parse_poker_game(game, [choice(actions)])
        elif isinstance(game._stage, ShowdownStage):
            parse_poker_game(game, ['s'])

    def create_game(self) -> NLTGame:
        return NLTGame(self.ANTE, self.BLINDS,
                       [randint(self.MIN_STACK, self.MAX_STACK) for _ in range(self.PLAYER_COUNT)])


if __name__ == '__main__':
    main()
