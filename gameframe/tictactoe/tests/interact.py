from gameframe.sequential.tests import interact_sequential
from gameframe.tictactoe import TicTacToeGame


def interact_tic_tac_toe():
    """Interacts with a tic tac toe game."""
    interact_sequential(TicTacToeGame)


if __name__ == '__main__':
    interact_tic_tac_toe()
