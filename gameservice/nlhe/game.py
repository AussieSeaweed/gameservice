from .actions import NLHENatureActions
from ..poker.game import PokerGame
from ..poker.actions import NLPlayerActions
from ..util.poker.deck import PokerDeck52
from ..util.poker.evaluator import Evaluator52
from ..exceptions import InvalidConfigException


class NLHEGame(PokerGame):
    player_actions_type = NLPlayerActions
    nature_actions_type = NLHENatureActions

    deck_type = PokerDeck52
    evaluator_type = Evaluator52

    def __init__(self):
        super().__init__()

        if self.blinds is None:
            raise InvalidConfigException
