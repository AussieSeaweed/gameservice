"""
This module allows interactions with custom no-limit texas hold'em games.
"""
from gameframe.sequential.tests.interact import sequential_interact
from gameframe.poker import LazyNLHEGame


class CustomNLHEGame(LazyNLHEGame):
    """
    This is a class that represents a custom no-limit texas hold'em games.
    """

    @property
    def ante(self):
        return 1

    @property
    def blinds(self):
        return [1, 2]

    @property
    def starting_stacks(self):
        return [200, 100, 50]


def main():
    sequential_interact(CustomNLHEGame)


if __name__ == '__main__':
    main()
