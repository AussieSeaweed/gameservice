import unittest
from abc import ABC, abstractmethod
from random import choice

from gameservice.poker import NLHEGame, PokerLazyNoLimit
from gameservice.tictactoe import TTTGame


class CustomNoLimit(PokerLazyNoLimit):
    def bet_amounts(self, player):
        amounts = super().bet_amounts(player)

        if len(amounts) == 2:
            lo, hi = amounts
            amounts = {lo, hi}

            for i in range(lo + 1, hi, 50):
                amounts.add(i)

            amounts = sorted(amounts)

        return amounts


class CustomHUNLHEGame(NLHEGame):
    @property
    def starting_stacks(self):
        return [200, 400]

    @property
    def blinds(self):
        return [1, 2]

    @property
    def ante(self):
        return 1

    def _create_limit(self):
        return CustomNoLimit()


class CustomNLHEGame(NLHEGame):
    @property
    def starting_stacks(self):
        return [200, 400, 400, 1000, 500, 400, 200, 200, 1000]

    @property
    def blinds(self):
        return [1, 2]

    @property
    def ante(self):
        return 1

    def _create_limit(self):
        return CustomNoLimit()


class GameTestMixin(ABC):
    @property
    @abstractmethod
    def num_monte_carlo_tests(self):
        pass

    @property
    @abstractmethod
    def game_type(self):
        pass

    @staticmethod
    @abstractmethod
    def check_game(game):
        pass

    def test_monte_carlo(self):
        for i in range(self.num_monte_carlo_tests):
            game = self.game_type()

            while not game.terminal:
                choice(game.player.actions).act()

            try:
                assert self.check_game(game)
            except AssertionError as e:
                print(game.nature.info_set)
                raise e


class PokerTestMixin(GameTestMixin, ABC):
    @staticmethod
    def check_game(game):
        return sum(game.starting_stacks) == sum(player.stack for player in game.players) and \
               all(player.stack >= 0 and player.bet >= 0 for player in game.players)


class NLHETestCase(unittest.TestCase, PokerTestMixin):
    @property
    def num_monte_carlo_tests(self):
        return 1000

    @property
    def game_type(self):
        return CustomNLHEGame


class HUNLHETestCase(unittest.TestCase, PokerTestMixin):
    @property
    def num_monte_carlo_tests(self):
        return 1000

    @property
    def game_type(self):
        return CustomNLHEGame


class TTTTestCase(unittest.TestCase, GameTestMixin):
    @property
    def num_monte_carlo_tests(self):
        return 1000

    @property
    def game_type(self):
        return TTTGame

    @staticmethod
    def check_game(game):
        return game.winner is not None or not game.empty_coords

    def test_tic_tac_toe_first_win(self):
        game = self.game_type()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([1, -1], payoffs)

    def test_tic_tac_toe_second_win(self):
        game = self.game_type()

        game.player.actions[8].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([-1, 1], payoffs)

    def test_tic_tac_toe_draw(self):
        game = self.game_type()

        game.player.actions[4].act()

        while not game.terminal:
            game.player.actions[0].act()

        payoffs = [player.payoff for player in game.players]

        self.assertEqual([0, 0], payoffs)


if __name__ == '__main__':
    unittest.main()
