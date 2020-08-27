from ..sequential.game import TurnQueueGame
from ..exceptions import InvalidNumPlayersException
from .player import PokerPlayer, PokerNature
from .context import PokerContext
from .players import PokerPlayers
from .street import Showdown, Distributing


class PokerGame(TurnQueueGame):
    min_num_players = 2

    player_type = PokerPlayer
    nature_type = PokerNature
    context_type = PokerContext

    players_type = PokerPlayers

    """Poker variables"""

    sb = 1
    bb = 2

    starting_stack = None

    street_types = None

    def __init__(self):
        super().__init__()

        if self.num_players < 2:
            raise InvalidNumPlayersException

        self.streets = [street_type(self) for street_type in self.street_types]

        self.winners = []
        self.winning_hand = None

    @property
    def street(self):
        return self.streets[0] if self.streets else None

    @property
    def player_actions_type(self):
        return self.street.player_actions_type

    @property
    def nature_actions_type(self):
        return self.street.nature_actions_type
