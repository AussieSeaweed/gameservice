from .actionsets import NLHENatureActionSet
from ..exceptions import GameConfigException
from ..poker.actionsets import NLPokerPlayerActionsSet
from ..poker.game import PokerGame
from ..utils.poker.decks import PokerDeck52
from ..utils.poker.evaluators import Evaluator52


class NLHEGame(PokerGame):
    nature_actionset_type = NLHENatureActionSet
    player_actionset_type = NLPokerPlayerActionsSet

    deck_type = PokerDeck52
    evaluator_type = Evaluator52

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not isinstance(self.blinds, list) or len(self.blinds) != 2:
            raise GameConfigException("NLHE requires 2 blinds")
