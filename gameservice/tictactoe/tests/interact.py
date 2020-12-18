"""
This module allows interactions with tic tac toe games.
"""
from gameservice.game.tests.interact import interact_seq
from gameservice.tictactoe import TTTGame


def main():
    interact_seq(TTTGame)


if __name__ == '__main__':
    main()
