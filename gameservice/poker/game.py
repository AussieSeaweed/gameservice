from ..sequential.game import TurnQueueGame
from .player import PokerPlayer, PokerNature
from .context import PokerContext
from .players import PokerPlayers


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

    def __init__(self, num_players=None):
        super().__init__(num_players)

        self.streets = [street_type(self) for street_type in self.street_types]

    @property
    def street(self):
        return self.streets[0] if self.streets else None

    @property
    def player_actions_type(self):
        return self.street.player_actions_type

    @property
    def nature_actions_type(self):
        return self.street.nature_actions_type

    def update(self):
        try:
            super().update()
        except IndexError:
            self.streets.pop(0)
            self.order.extend(self.street.order)
