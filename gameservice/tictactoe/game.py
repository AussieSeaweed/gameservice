from .actionset import TicTacToeActionSet
from .context import TicTacToeContext
from .players import TicTacToePlayer, TicTacToeNature
from ..game.actionset import EmptyActionSet
from ..game.playerset import PlayerSet
from ..sequential.game import SequentialGame


class TicTacToeGame(SequentialGame):
    player_type = TicTacToePlayer
    nature_type = TicTacToeNature
    context_type = TicTacToeContext

    num_players = 2
    playerset_type = PlayerSet

    player_actionset_type = TicTacToeActionSet
    nature_actionset_type = EmptyActionSet

    def _get_initial_player(self):
        return self.players[0]
