from __future__ import annotations

from typing import List, Dict, Any

from ..game.environment import Environment


class PokerEnvironment(Environment):
    def __init__(self):
        self.pot: int = 0
        self.board: List[str] = []

    def get_info(self) -> Dict[str, Any]:
        return {
            "pot": self.pot,
            "board": self.board
        }
