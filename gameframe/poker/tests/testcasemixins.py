from abc import ABC

from gameframe.sequential.tests.testcasemixins import SequentialTestCaseMixin


class PokerTestCaseMixin(SequentialTestCaseMixin, ABC):
    """
    This is a mixin for poker test cases.
    """

    @staticmethod
    def validate_game(game):
        return sum(game.starting_stacks) == sum(player.stack for player in game.players) and all(
            player.stack >= 0 and player.bet >= 0 for player in game.players)

    @property
    def num_monte_carlo_tests(self):
        return 1000
