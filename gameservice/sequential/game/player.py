from abc import abstractmethod, ABC
from typing import Dict, Any


class Player(ABC):
    def __init__(self, index: int):
        self.index: int = index

    def info(self, show_private: bool) -> Dict[str, Any]:
        return {
            "index": self.index,
        }
