from collections import defaultdict

from .context import PokerContext
from .players import PokerPlayers
from ..exceptions import InvalidNumPlayersException
from ..sequential.game import SequentialGame


class PokerGame(SequentialGame):
    context_type = PokerContext
    players_type = PokerPlayers

    """Poker variables"""

    sb = None
    bb = None

    deck_type = None
    evaluator_type = None

    starting_stacks = None

    def __init__(self):
        super().__init__()

        if self.num_players < 2:
            raise InvalidNumPlayersException

        self.deck = self._create_deck()
        self.evaluator = self._create_evaluator()
        self.player = self.players.nature

        self.street = 0

        self.chance_players = []
        self.aggressor = None
        self.min_raise = None

        self.results = defaultdict(lambda: [])

    @property
    def num_players(self):
        return len(self.starting_stacks)

    def _create_deck(self):
        return self.deck_type()

    def _create_evaluator(self):
        return self.evaluator_type()

    def evaluate(self, card_str_list):
        return self.evaluator.evaluate(card_str_list)

    def bet_sizes(self, min_raise, max_raise):
        return range(min_raise, max_raise + 1)
