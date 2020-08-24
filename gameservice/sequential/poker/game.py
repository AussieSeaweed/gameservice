from .environment import PokerEnvironment
from .logic import PokerLogic
from .player import PokerPlayer
from ..game import SequentialGame


class Poker(SequentialGame):
    min_num_players = 2
    max_num_players = 9

    player_type = PokerPlayer
    environment_type = PokerEnvironment
    logic_type = PokerLogic

    """Poker class member variables"""

    starting_stack: int

    def create_player(self, index: int):
        return self.player_type(index, self.starting_stack)
