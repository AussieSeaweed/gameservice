from random import randint, sample
from typing import cast
from unittest import TestCase, main

from gameframe.game import ActionException
from gameframe.poker import NLTHEGame, PokerPlayer
from gameframe.poker.stages import BettingStage, DealingStage, ShowdownStage
from gameframe.sequential.tests.test_monte_carlo import MCTestCaseMixin


class NLTexasHEMCTestCase(TestCase, MCTestCaseMixin[NLTHEGame]):
    ANTE = 1
    BLINDS = [1, 2]
    PLAYER_COUNT = 4
    MIN_STACK = 0
    MAX_STACK = 10

    mc_test_count = 1000

    def verify(self, game: NLTHEGame) -> None:
        super().verify(game)

        if game.is_terminal:
            assert game.pot == 0
            assert all(player.bet == 0 for player in game.players)
            assert all(player.stack >= 0 for player in game.players)

    def act(self, game: NLTHEGame) -> None:
        if isinstance(game._stage, DealingStage):
            hole_card_count = len(game._stage.hole_card_statuses)
            board_card_count = game._stage.board_card_count

            if hole_card_count:
                for player in game.players:
                    game.nature.deal_player(player, *sample(list(game._deck), hole_card_count))

            if board_card_count:
                game.nature.deal_board(*sample(list(game._deck), board_card_count))
        elif isinstance(game._stage, BettingStage):
            actor = cast(PokerPlayer, game.actor)

            try:
                actor.bet_raise(2 * max(player.bet for player in game.players))
                return
            except ActionException:
                pass

            try:
                actor.fold()
                return
            except ActionException:
                pass

            actor.check_call()
        elif isinstance(game._stage, ShowdownStage):
            cast(PokerPlayer, game.actor).showdown()

    def create_game(self) -> NLTHEGame:
        return NLTHEGame(self.ANTE, self.BLINDS,
                         [randint(self.MIN_STACK, self.MAX_STACK) for _ in range(self.PLAYER_COUNT)])


if __name__ == '__main__':
    main()
