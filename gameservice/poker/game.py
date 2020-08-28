from .context import PokerContext
from .player import PokerPlayer
from .players import PokerPlayers
from ..exceptions import InvalidNumPlayersException
from ..sequential.game import SequentialGame


class PokerGame(SequentialGame):
    player_type = PokerPlayer
    context_type = PokerContext

    players_type = PokerPlayers

    """Poker variables"""

    sb = None
    bb = None

    starting_stack = None

    num_players = None

    deck_type = None
    evaluate = None

    def __init__(self):
        super().__init__()

        if self.num_players < 2:
            raise InvalidNumPlayersException

        self.deck = self._create_deck()
        self.player = self.players.nature

        self.phase = -1

        self.aggressor = None
        self.min_raise = self.sb

        self.winners = []
        self.winning_hand = None

    def _create_deck(self):
        return self.deck_type()

    def next(self):
        self.context.pot += sum(self.players.bets)

        for player in self.players:
            player.bet = 0

        self.player = self.players.nature

        self.phase += 1
