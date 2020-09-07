from .actions import NLHENatureActions
from ..poker.game import PokerGame
from ..poker.player import BlindedPokerPlayer
from ..poker.actions import NLPlayerActions
from ..util.poker.deck import PokerDeck52
from ..util.poker.evaluator import Evaluator52


class NLHEGame(PokerGame):
    player_type = BlindedPokerPlayer

    player_actions_type = NLPlayerActions
    nature_actions_type = NLHENatureActions

    deck_type = PokerDeck52
    evaluator_type = Evaluator52

    def bet_sizes(self, min_raise, max_raise):
        return range(min_raise, max_raise + 1)
