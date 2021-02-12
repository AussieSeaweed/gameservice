from random import choice
from unittest import TestCase, main

from gameframe.game.tests.test_monte_carlo import MCTestCaseMixin
from gameframe.rockpaperscissors import RPSGame, RPSHand


class RPSMCTestCase(TestCase, MCTestCaseMixin[RPSGame]):
    MC_TEST_COUNT = 100000

    def act(self, game: RPSGame) -> None:
        for player in game.players:
            player.throw(choice(list(RPSHand)))

    def create_game(self) -> RPSGame:
        return RPSGame()


if __name__ == '__main__':
    main()
