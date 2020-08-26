from ..sequential.game import TurnAlternationGame

from .context import TicTacToeContext
from .actions import TicTacToeActions


class TicTacToe(TurnAlternationGame):
    min_num_players = 2
    max_num_players = 2
    num_players = 2
    context_type = TicTacToeContext
    player_actions_type = TicTacToeActions

    @property
    def terminal(self):
        return self.context.winning_coords is not None or not self.context.empty_coords
