from itertools import filterfalse
from random import randint
from unittest import TestCase, main

from auxiliary import const, next_or_none

from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand, RockPaperScissorsPlayer
from gameframe.tests import GameFrameTestCaseMixin


class RockPaperScissorsTestCase(GameFrameTestCaseMixin, TestCase):
    def create_game(self):
        return RockPaperScissorsGame(randint(2, 5))

    def act(self, game):
        next(filterfalse(RockPaperScissorsPlayer.hand.fget, game.players)).throw()

    def verify(self, game):
        if game.is_terminal():
            self.assertTrue(all(map(RockPaperScissorsPlayer.hand.fget, game.players)))

            winner = next_or_none(game.winners)

            if winner is None:
                self.assertTrue(
                    const(map(RockPaperScissorsPlayer.hand.fget, game.players))
                    or set(map(RockPaperScissorsPlayer.hand.fget, game.players)) == set(RockPaperScissorsHand),
                )
            else:
                for player in game.players:
                    self.assertLessEqual(player.hand, winner.hand)
        else:
            self.assertFalse(all(map(RockPaperScissorsPlayer.hand.fget, game.players)))

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
