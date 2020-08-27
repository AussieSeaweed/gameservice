from .actions import TicTacToeActions
from .context import TicTacToeContext
from ..sequential.game import SequentialGame


class TicTacToe(SequentialGame):
    num_players = 2
    context_type = TicTacToeContext
    player_actions_type = TicTacToeActions

    def __init__(self):
        super().__init__()

        self.player = self.players[0]
