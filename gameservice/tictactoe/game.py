from .actions import TicTacToeActions
from .context import TicTacToeContext
from .player import TicTacToePlayer, TicTacToeNature
from ..game.actions import EmptyActions
from ..game.players import Players
from ..sequential.game import SequentialGame


class TicTacToeGame(SequentialGame):
    player_type = TicTacToePlayer
    nature_type = TicTacToeNature
    context_type = TicTacToeContext

    num_players = 2
    players_type = Players

    player_actions_type = TicTacToeActions
    nature_actions_type = EmptyActions

    def _get_initial_player(self):
        return self.players[0]
