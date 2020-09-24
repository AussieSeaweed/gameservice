from .context import PokerContext
from .players import PokerPlayer, PokerNature
from .playerset import PokerPlayerSet
from ..exceptions import InvalidNumPlayersException
from ..sequential.game import SequentialGame


class PokerGame(SequentialGame):
    player_type = PokerPlayer
    nature_type = PokerNature
    context_type = PokerContext

    playerset_type = PokerPlayerSet

    """Poker variables"""

    deck_type = None
    evaluator_type = None

    ante = None
    blinds = None
    starting_stacks = None

    def __init__(self):
        super().__init__()

        if self.num_players < 2:
            raise InvalidNumPlayersException

        self.deck = self.deck_type()
        self.evaluator = self.evaluator_type()

    def _get_initial_player(self):
        return self.players.nature

    @property
    def num_players(self):
        return len(self.starting_stacks)

    def evaluate(self, card_str_list):
        return self.evaluator.evaluate(card_str_list)

    def bet_sizes(self, min_raise, max_raise):
        return range(min_raise, max_raise + 1)
