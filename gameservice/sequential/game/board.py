from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .game import SequentialGame


class Board(ABC):
    def __init__(self, game: SequentialGame):
        self.game: SequentialGame = game

    @property
    @abstractmethod
    def info(self) -> Dict[str, Any]:
        pass
