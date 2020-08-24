from __future__ import annotations

from typing import List, Dict, Any, TYPE_CHECKING

from ..game.environment import Environment

if TYPE_CHECKING:
    from .game import Poker


class PokerEnvironment(Environment):
    def __init__(self, game: Poker):
        super().__init__(game)

        self.pot: int = 0
        self.board: List[str] = []

    @property
    def info(self) -> Dict[str, Any]:
        return {
            "pot": self.pot,
            "board": self.board
        }
