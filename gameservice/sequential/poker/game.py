from typing import List, Optional

from .environment import PokerEnvironment
from .logic import PokerLogic
from .player import PokerPlayer
from ..game import SequentialGame


class Poker(SequentialGame):
    min_num_players = 2

    player_type = PokerPlayer
    environment_type = PokerEnvironment
    logic_type = PokerLogic

    """Poker class member variables"""

    starting_stack: int

    """Type hinting"""

    players: List[Optional[PokerPlayer]]
    environment: PokerEnvironment
    logic: PokerLogic
