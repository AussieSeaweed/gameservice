from random import choice
from unittest import TestCase

from gameframe.rockpaperscissors import RockPaperScissors, RockPaperScissorsHand
from gameframe.tests.utilities import MonteCarloTestCaseMixin


class RockPaperScissorsTest(MonteCarloTestCaseMixin[RockPaperScissors], TestCase):
    monte_carlo_test_count = 100000

    def create_game(self) -> RockPaperScissors:
        return RockPaperScissors()

    def act(self, game: RockPaperScissors) -> None:
        for player in game.players:
            player.play(choice(tuple(RockPaperScissorsHand)))

    def verify(self, game: RockPaperScissors) -> None:
        if game.is_terminal():
            if game.winner is game.players[0]:
                self.assertGreater(game.players[0].hand, game.players[1].hand)
            elif game.winner is game.players[1]:
                self.assertLess(game.players[0].hand, game.players[1].hand)
            else:
                self.assertEqual(game.players[0].hand, game.players[1].hand)
        else:
            self.assertTrue(game.players[0].hand is None or game.players[1].hand is None)
