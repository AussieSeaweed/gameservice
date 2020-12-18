from abc import ABC

from gameservice.game.tests.testcasemixins import SeqTestCaseMixin


class PokerTestCaseMixin(SeqTestCaseMixin, ABC):
    """
    This is a mixin for poker test cases.
    """

    @staticmethod
    def validate_game(game):
        """
        Validates the integrity of the poker game.
        :param game: a poker game of the poker test case
        :return: a boolean value of the validity of the poker game
        """
        return sum(game.starting_stacks) == sum(player.stack for player in game.players) and all(
            player.stack >= 0 and player.bet >= 0 for player in game.players)

    @property
    def num_monte_carlo_tests(self):
        """
        :return: the number of monte carlo tests of poker games
        """
        return 1000
