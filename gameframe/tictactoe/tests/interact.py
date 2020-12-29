"""
This module allows interactions with tic tac toe games.
"""
from gameframe.sequential.tests import sequential_interact
from gameframe.tictactoe import TicTacToeGame


def main():
    sequential_interact(TicTacToeGame)


if __name__ == '__main__':
    main()
