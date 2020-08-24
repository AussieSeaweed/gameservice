from __future__ import annotations

from typing import List, TYPE_CHECKING

from gameservice.exceptions import NotTerminalGameError
from ..game.logic import TurnQueueLogic, ChanceLogic, NestedLogic
from .action import NoLimitPut, Continue, Surrender, Deal, Peel, Distribute

if TYPE_CHECKING:
    from .game import Poker


class PokerLogic(NestedLogic):
    """Type hinting"""

    game: Poker


class DealLogic(TurnQueueLogic):
    """Type hinting"""

    game: Poker


class PeelLogic(ChanceLogic):
    """Type hinting"""

    game: Poker


class ShowdownLogic(TurnQueueLogic):
    """Type hinting"""

    game: Poker
