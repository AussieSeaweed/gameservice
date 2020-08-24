from __future__ import annotations

from typing import List, TYPE_CHECKING

from gameservice.exceptions import NotTerminalGameError
from ..game.logic import TurnQueueLogic, NestedLogic
from .action import NoLimitPut, Continue, Surrender, Deal, Peel, Distribute

if TYPE_CHECKING:
    from .game import Poker


class PokerLogic(NestedLogic):
    """Type hinting"""

    game: Poker


class DealLogic(TurnQueueLogic):
    """Type hinting"""

    game: Poker


class ShowdownLogic(TurnQueueLogic):
    """Type hinting"""

    game: Poker


class PeelLogic(TurnQueueLogic):
    """Type hinting"""

    game: Poker


class BettingLogic(TurnQueueLogic):
    """Static member variables"""



    """Type hinting"""

    game: Poker
