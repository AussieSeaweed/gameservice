from .context import PokerContext
from .player import PokerPlayer, PokerNature
from .players import PokerPlayers
from ..exceptions import InvalidNumPlayersException
from ..sequential.game import SequentialGame


class PokerGame(SequentialGame):
    player_type = PokerPlayer
    nature_type = PokerNature
    context_type = PokerContext

    players_type = PokerPlayers

    """Poker variables"""

    num_players = None

    sb = None
    bb = None

    starting_stacks = None

    deck_type = None
    evaluator_type = None

    def __init__(self):
        super().__init__()

        if self.num_players < 2:
            raise InvalidNumPlayersException

        self.deck = self._create_deck()
        self.evaluator = self._create_evaluator()
        self.player = self.players.nature

        self.street = 0

        self.aggressor = None
        self.min_raise = None

        self.winners = []
        self.winning_hand = None

    def _create_deck(self):
        return self.deck_type()

    def _create_evaluator(self):
        return self.evaluator_type()

    def evaluate(self, card_str_list):
        return self.evaluator.evaluate(card_str_list)
