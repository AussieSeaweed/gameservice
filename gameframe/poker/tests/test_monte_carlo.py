# from random import choices, randint, random
# from typing import cast
# from unittest import TestCase, main
#
# from gameframe.poker import NLTexasHEGame, PokerPlayer
# from gameframe.poker.stages import BettingStage, DealingStage, SetupStage, ShowdownStage
# from gameframe.sequential.tests.test_monte_carlo import MCTestCaseMixin
#
#
# class NLTexasHEMCTestCase(TestCase, MCTestCaseMixin[NLTexasHEGame]):
#     ANTE = 1
#     BLINDS = [1, 2]
#     PLAYER_COUNT = 4
#     MIN_STACK = 0
#     MAX_STACK = 100
#
#     @property
#     def mc_test_count(self) -> int:
#         return 10
#
#     def verify(self, game: NLTexasHEGame) -> None:
#         super().verify(game)
#
#         assert game.env.pot + sum(player.bet + player.stack for player in game.players) \
#                == sum(player._total for player in game.players), f'{game.players}\n{game.env}'
#
#     def act(self, game: NLTexasHEGame) -> None:
#         if isinstance(game.env._stage, SetupStage):
#             game.nature.setup()
#         elif isinstance(game.env._stage, DealingStage):
#             hole_card_count = len(game.env._stage.hole_card_statuses)
#             board_card_count = game.env._stage.board_card_count
#
#             if hole_card_count:
#                 for player in game.players:
#                     game.nature.deal_player(player, *choices(list(game.env._deck), k=hole_card_count))
#
#             if board_card_count:
#                 game.nature.deal_board(*choices(list(game.env._deck), k=board_card_count))
#         elif isinstance(game.env._stage, BettingStage):
#             player = cast(PokerPlayer, game.env.actor)
#             n = randint(0, 2)
#
#             if n == 0:
#                 try:
#                     player.fold()
#                     return
#                 except ValueError:
#                     pass
#             elif n == 1:
#                 try:
#                     player.bet_raise(randint(game.env._stage.min_amount, game.env._stage.max_amount))
#                     return
#                 except ValueError:
#                     pass
#
#             player.check_call()
#         elif isinstance(game.env._stage, ShowdownStage):
#             cast(PokerPlayer, game.env.actor).showdown()
#         else:
#             game.nature.distribute()
#
#     def create_game(self) -> NLTexasHEGame:
#         return NLTexasHEGame(self.ANTE, self.BLINDS,
#                              [randint(self.MIN_STACK, self.MAX_STACK) for _ in range(self.PLAYER_COUNT)])
#
#
# if __name__ == '__main__':
#     main()
