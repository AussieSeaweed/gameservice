from .actionset import NLHENatureActionSet
from ..exceptions import InvalidConfigException
from ..poker.actionset import NLPlayerActionSet
from ..poker.game import PokerGame
from ..utils.poker.deck import PokerDeck52
from ..utils.poker.evaluator import Evaluator52


class NLHEGame(PokerGame):
    label = "No-Limit Texas Hold'em"

    player_actionset_type = NLPlayerActionSet
    nature_actionset_type = NLHENatureActionSet

    deck_type = PokerDeck52
    evaluator_type = Evaluator52

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.blinds is None:
            raise InvalidConfigException
