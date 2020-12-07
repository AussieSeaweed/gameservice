import unittest
from abc import ABC, abstractmethod
from random import choice, randint

from gameservice.poker import NLHELazyGame
from gameservice.tictactoe import TTTGame


# Game Classes and Mixins


class CustomNLHEGame(NLHELazyGame):
    def __init__(self):
        self.__starting_stacks = [randint(self.min_starting_stack, self.max_starting_stack) for _ in
                                  range(self.num_players)]

        super().__init__()

    @property
    def blinds(self):
        return [1, 2]

    @property
    def ante(self):
        return 1

    @property
    def min_starting_stack(self):
        return 0

    @property
    def max_starting_stack(self):
        return 1000

    @property
    def starting_stacks(self):
        return self.__starting_stacks

    @property
    @abstractmethod
    def num_players(self):
        pass


class CustomNLHE2Game(CustomNLHEGame):
    @property
    def num_players(self):
        return 2


class CustomNLHE6Game(CustomNLHEGame):
    @property
    def num_players(self):
        return 6


class CustomNLHE9Game(CustomNLHEGame):
    @property
    def num_players(self):
        return 9


# Game Test Mixins


class GameTestCaseMixin(ABC):
    @staticmethod
    @abstractmethod
    def create_game():
        pass

    @staticmethod
    @abstractmethod
    def check_game(game):
        pass


class SeqTestCaseMixin(GameTestCaseMixin, ABC):
    @property
    @abstractmethod
    def num_monte_carlo_tests(self):
        pass

    def test_monte_carlo(self):
        for i in range(self.num_monte_carlo_tests):
            game = self.create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            try:
                assert self.check_game(game)
            except AssertionError as e:
                print(game.nature.info_set)
                raise e


class PokerTestCaseMixin(SeqTestCaseMixin, ABC):
    @property
    def num_monte_carlo_tests(self):
        return 1000

    @staticmethod
    def check_game(game):
        return sum(game.starting_stacks) == sum(player.stack for player in game.players) and \
               all(player.stack >= 0 and player.bet >= 0 for player in game.players)


# Game Test Cases


class TTTTestCase(unittest.TestCase, GameTestCaseMixin):
    @staticmethod
    def create_game():
        return TTTGame()

    @staticmethod
    def check_game(game):
        return game.winner is not None or not game.empty_coords

    @property
    def num_monte_carlo_tests(self):
        return 1000

    def test_tic_tac_toe_first_win(self):
        game = self.create_game()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([1, -1], payoffs)

    def test_tic_tac_toe_second_win(self):
        game = self.create_game()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([-1, 1], payoffs)

    def test_tic_tac_toe_draw(self):
        game = self.create_game()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([0, 0], payoffs)


class NLHE2TestCase(unittest.TestCase, PokerTestCaseMixin):
    @staticmethod
    def create_game():
        return CustomNLHE2Game()


class NLHE6TestCase(unittest.TestCase, PokerTestCaseMixin):
    @staticmethod
    def create_game():
        return CustomNLHE6Game()


class NLHE9TestCase(unittest.TestCase, PokerTestCaseMixin):
    @staticmethod
    def create_game():
        return CustomNLHE9Game()


if __name__ == '__main__':
    unittest.main()
