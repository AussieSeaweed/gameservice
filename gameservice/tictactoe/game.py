from ..sequential.game import TurnAlternationGame

from .context import TicTacToeContext
from .actions import TicTacToeActions


class TicTacToe(TurnAlternationGame):
    num_players = 2
    context_type = TicTacToeContext
    player_actions_type = TicTacToeActions
    initial_turn = 0

    def __init__(self):
        super().__init__()

    @property
    def terminal(self):
        return super().terminal or self.context.winning_coords is not None or not self.context.empty_coords
