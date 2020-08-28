from .actions import NLHEPlayerActions, NLHENatureActions
from ..poker.game import PokerGame
from ..util.poker.deck import PokerDeck52
from ..util.poker.evaluate import evaluate52


class NLHEGame(PokerGame):
    player_actions_type = NLHEPlayerActions
    nature_actions_type = NLHENatureActions

    deck_type = PokerDeck52
    evaluate = evaluate52
