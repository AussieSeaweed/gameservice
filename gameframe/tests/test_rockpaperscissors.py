from random import choice
from unittest import TestCase, main

from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand
from gameframe.tests import GameFrameTestCaseMixin


class RockPaperScissorsTest(GameFrameTestCaseMixin, TestCase):
    MONTE_CARLO_TEST_COUNT = 10000
    SPEED_TEST_TIME = 1

    def create_game(self):
        return RockPaperScissorsGame()

    def act(self, game):
        player = choice(tuple(player for player in game.players if player.hand is None))
        player.throw(choice(tuple(RockPaperScissorsHand)))

    def verify(self, game):
        if game.is_terminal():
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


if __name__ == '__main__':
    main()
