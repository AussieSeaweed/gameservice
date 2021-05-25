from random import choice
from unittest import TestCase

from gameframe.rockpaperscissors import RockPaperScissors, RockPaperScissorsHand
from gameframe.tests import GameFrameTestCaseMixin


class RockPaperScissorsTest(GameFrameTestCaseMixin[RockPaperScissors], TestCase):
    monte_carlo_test_count = 10000
    speed_test_time = 1

    def create_game(self) -> RockPaperScissors:
        return RockPaperScissors()

    def act(self, game: RockPaperScissors) -> None:
        player = choice(tuple(player for player in game.players if player.hand is None))
        player.throw(choice(tuple(RockPaperScissorsHand)))

    def verify(self, game: RockPaperScissors) -> None:
        if game.terminal:
            self.assertTrue(game.players[0].hand is not None or game.players[1].hand is not None)

            if game.winner is game.players[0]:
                self.assertGreater(game.players[0].hand, game.players[1].hand)
            elif game.winner is game.players[1]:
                self.assertLess(game.players[0].hand, game.players[1].hand)
            else:
                self.assertEqual(game.players[0].hand, game.players[1].hand)
        else:
            self.assertTrue(game.players[0].hand is None or game.players[1].hand is None)

        for player in game.players:
            if player.hand is None:
                self.assertTrue(player.can_throw())
            else:
                self.assertFalse(player.can_throw())

            for hand in RockPaperScissorsHand:
                if player.hand is None:
                    self.assertTrue(player.can_throw(hand))
                else:
                    self.assertFalse(player.can_throw(hand))
