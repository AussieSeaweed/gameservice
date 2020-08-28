from .actions import TicTacToeActions
from .context import TicTacToeContext
from .players import TicTacToePlayers
from ..sequential.game import SequentialGame


class TicTacToe(SequentialGame):
    context_type = TicTacToeContext
    players_type = TicTacToePlayers

    player_actions_type = TicTacToeActions

    def __init__(self):
        super().__init__()

        self.player = self.players[0]
