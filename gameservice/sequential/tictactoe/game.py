from .environment import TicTacToeEnvironment
from .logic import TicTacToeLogic
from ..game import SequentialGame
from ..game.player import Player


class TicTacToe(SequentialGame):
    min_num_players = 2
    max_num_players = 2

    player_type = Player
    environment_type = TicTacToeEnvironment
    logic_type = TicTacToeLogic
