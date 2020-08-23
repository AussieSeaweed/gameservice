from ..game import SequentialGame, Player
from .environment import TicTacToeEnvironment
from .logic import TicTacToeLogic


class TicTacToe(SequentialGame):
    min_num_players = 2
    max_num_players = 2

    player_type = Player
    environment_type = TicTacToeEnvironment
    logic_type = TicTacToeLogic

    """Type hinting"""

    player: Player
    environment: TicTacToeEnvironment
    logic: TicTacToeLogic
