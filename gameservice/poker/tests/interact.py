"""
This module allows interactions with custom no-limit texas hold'em games.
"""
from gameservice.game.tests.interact import interact_seq
from gameservice.poker import LazyNLHEGame


class CustomNLHEGame(LazyNLHEGame):
    """
    This is a class that represents a custom no-limit texas hold'em games.
    """

    @property
    def ante(self):
        return 0

    @property
    def blinds(self):
        return [1, 2]

    @property
    def starting_stacks(self):
        return [300, 200, 100]


def main():
    interact_seq(CustomNLHEGame)


if __name__ == '__main__':
    main()
