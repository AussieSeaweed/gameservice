from collections.abc import Sequence

from gameframe.sequential.tests import interact_sequential
from gameframe.tictactoe import TicTacToeGame

__all__: Sequence[str] = ['interact_tic_tac_toe']


def interact_tic_tac_toe() -> None:
    """Interacts with a tic tac toe game."""
    interact_sequential(TicTacToeGame)


if __name__ == '__main__':
    interact_tic_tac_toe()
