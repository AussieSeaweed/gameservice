from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Dict, Optional, Any, TYPE_CHECKING

from gameservice.exceptions import InvalidActionException

if TYPE_CHECKING:
    from .game import SequentialGame


class Action(ABC):
    def __init__(self, *args):
        pass

    @classmethod
    @abstractmethod
    def info(cls, game: SequentialGame) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def valid(self, game: SequentialGame) -> bool:
        pass

    def apply(self, game: SequentialGame) -> None:
        if not self.valid(game):
            raise InvalidActionException
