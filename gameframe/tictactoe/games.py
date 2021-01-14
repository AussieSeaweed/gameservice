from gameframe.sequential import SequentialGame
from gameframe.tictactoe.actors import TicTacToeNature, TicTacToePlayer
from gameframe.tictactoe.environments import TicTacToeEnvironment


class TicTacToeGame(SequentialGame):
    """TicTacToeGame is the class for tic tac toe games."""

    def __init__(self):
        super().__init__(
            TicTacToeEnvironment(self),
            TicTacToeNature(self),
            (TicTacToePlayer(self), TicTacToePlayer(self)),
            0,
        )
