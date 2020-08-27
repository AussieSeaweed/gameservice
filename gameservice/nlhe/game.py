from ..sequential.game import TurnQueueGame
from ..exceptions import InvalidNumPlayersException
from ..poker.player import PokerPlayer
from ..poker.context import PokerContext
from ..poker.players import PokerPlayers


class NLHEGame(TurnQueueGame):
    min_num_players = 2

    player_type = PokerPlayer
    context_type = PokerContext

    players_type = PokerPlayers

    player_actions_type = None
    nature_actions_type = None

    """NLHE variables"""

    sb = 1
    bb = 2

    starting_stack = None

    num_streets = 4

    def __init__(self):
        super().__init__()

        if self.num_players < 2:
            raise InvalidNumPlayersException

        self.order = [None]
        self.chance = None

        self.__street = 0

        self.winners = []
        self.winning_hand = None

    @property
    def street(self):
        return self.__street

    def next(self):
        self.context.pot += sum(self.players.bets)
        self.players.clear_bets()

        self.order = [None]
        self.chance = None

        self.__street += 1
