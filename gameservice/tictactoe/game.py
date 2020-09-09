from .actions import TicTacToeActions
from .context import TicTacToeContext
from .players import TicTacToePlayers
from ..sequential.game import SequentialGame
from ..game.actions import EmptyActions


class TicTacToeGame(SequentialGame):
    context_type = TicTacToeContext
    players_type = TicTacToePlayers

    player_actions_type = TicTacToeActions
    nature_actions_type = EmptyActions

    def __init__(self):
        super().__init__()

        self.player = self.players[0]
