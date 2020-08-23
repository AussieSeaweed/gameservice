from __future__ import annotations

from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .game import SequentialGame


class Player:
    def __init__(self, game: SequentialGame, index: int):
        self.game: SequentialGame = game
        self.index: int = index

    def info(self, show_private: bool) -> Dict[str, Any]:
        return {
            "index": self.index,
        }
