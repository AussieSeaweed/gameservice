"""
This module allows interactions with tic tac toe games.
"""
from gameservice.game.tests.interact import sequential_interact
from gameservice.tictactoe import TicTacToeGame


def main():
    sequential_interact(TicTacToeGame)


if __name__ == '__main__':
    main()
