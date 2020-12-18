"""
This module allows interactions with tic tac toe games.
"""
from gameservice.game.tests.interact import interact_seq
from gameservice.poker import LazyNLHEGame


class CustomNLHEGame(LazyNLHEGame):
    @property
    def ante(self):
        pass

    @property
    def blinds(self):
        pass

    @property
    def starting_stacks(self):
        pass


def main():
    interact_seq(CustomNLHEGame)


if __name__ == '__main__':
    main()
