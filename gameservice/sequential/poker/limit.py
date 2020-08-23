from abc import ABC

from .game import PokerGame
from .action import NoLimitPut, Continue, Surrender


class NoLimit(PokerGame, ABC):
    action_set = {
        "put": NoLimitPut,
        "continue": Continue,
        "surrender": Surrender
    }
