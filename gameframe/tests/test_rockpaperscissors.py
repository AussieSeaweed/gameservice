from itertools import filterfalse, product
from random import randint
from unittest import TestCase, main

from auxiliary import const, next_or_none

from gameframe.games.rockpaperscissors import RockPaperScissorsGame, RockPaperScissorsHand, RockPaperScissorsPlayer
from gameframe.tests import GameFrameTestCaseMixin


class RockPaperScissorsTestCase(GameFrameTestCaseMixin, TestCase):
    def test_heads_up(self):
        game = RockPaperScissorsGame()
        game.players[0].throw(RockPaperScissorsHand.ROCK)
        game.players[1].throw(RockPaperScissorsHand.SCISSORS)
        self.assertIs(next(game.winners), game.players[0])
        self.assertIs(next(game.losers), game.players[1])

        game = RockPaperScissorsGame()
        game.players[0].throw(RockPaperScissorsHand.PAPER)
        game.players[1].throw(RockPaperScissorsHand.SCISSORS)
        self.assertIs(next(game.winners), game.players[1])
        self.assertIs(next(game.losers), game.players[0])

        game = RockPaperScissorsGame()
        game.players[0].throw(RockPaperScissorsHand.PAPER)
        game.players[1].throw(RockPaperScissorsHand.PAPER)
        self.assertIs(next_or_none(game.winners), None)
        self.assertIs(next_or_none(game.losers), None)

    def test_non_heads_up(self):
        game = RockPaperScissorsGame(3)

        for player, hand_str in zip(game.players, ('Rock', 'Paper', 'Scissors')):
            player.throw(RockPaperScissorsHand(hand_str))

        self.assertSequenceEqual(tuple(game.winners), ())
        self.assertSequenceEqual(tuple(game.losers), ())

        game = RockPaperScissorsGame(4)

        for player, hand_str in zip(game.players, ('Rock', 'Paper', 'Rock', 'Rock')):
            player.throw(RockPaperScissorsHand(hand_str))

        self.assertSequenceEqual(tuple(game.winners), (game.players[1],))
        self.assertSequenceEqual(tuple(game.losers), (game.players[0], *game.players[2:]))

        game = RockPaperScissorsGame(5)

        for player, hand_str in zip(game.players, ('Rock', 'Paper', 'Scissors', 'Rock', 'Paper')):
            player.throw(RockPaperScissorsHand(hand_str))

        self.assertSequenceEqual(tuple(game.winners), ())
        self.assertSequenceEqual(tuple(game.losers), ())

        game = RockPaperScissorsGame(6)

        for player, hand_str in zip(game.players, ('Paper', 'Paper', 'Rock', 'Rock', 'Paper', 'Paper')):
            player.throw(RockPaperScissorsHand(hand_str))

        self.assertSequenceEqual(tuple(game.winners), game.players[:2] + game.players[4:])
        self.assertSequenceEqual(tuple(game.losers), game.players[2:4])

    def create_game(self):
        return RockPaperScissorsGame(randint(2, 5))

    def act(self, game):
        next(filterfalse(RockPaperScissorsPlayer.hand.fget, game.players)).throw()

    def verify(self, game):
        if game.is_terminal():
            self.assertTrue(all(map(RockPaperScissorsPlayer.hand.fget, game.players)))

            winner = next_or_none(game.winners)
            loser = next_or_none(game.losers)

            if winner is None:
                self.assertTrue(
                    const(map(RockPaperScissorsPlayer.hand.fget, game.players))
                    or set(map(RockPaperScissorsPlayer.hand.fget, game.players)) == set(RockPaperScissorsHand),
                )
            else:
                for player in game.players:
                    self.assertLessEqual(player.hand, winner.hand)

            self.assertTrue((winner is None) == (loser is None))

            for winner, loser in product(game.winners, game.losers):
                self.assertGreater(winner.hand, loser.hand)
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
