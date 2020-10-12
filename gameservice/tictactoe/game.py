from .actionsets import TicTacToeActionSet
from .context import TicTacToeContext
from .players import TicTacToePlayer
from ..game.actionsets import EmptyActionSet
from ..game.players import ZeroSumNature
from ..game.playersets import PlayerSet
from ..sequential.game import SequentialGame


class TicTacToeGame(SequentialGame):
    num_players = 2

    context_type = TicTacToeContext

    nature_type = ZeroSumNature
    player_type = TicTacToePlayer
    playerset_type = PlayerSet

    nature_actionset_type = EmptyActionSet
    player_actionset_type = TicTacToeActionSet

    def _get_initial_player(self):
        return self.players[0]
