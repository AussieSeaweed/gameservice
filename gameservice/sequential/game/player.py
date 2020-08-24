from __future__ import annotations

from typing import Dict, Any


class Player:
    def __init__(self, index: int):
        self.index: int = index

    def get_info(self, show_private: bool) -> Dict[str, Any]:
        return {
            "index": self.index,
        }
