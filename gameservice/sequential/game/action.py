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
    def get_info(cls, game: SequentialGame) -> Optional[Dict[str, Any]]:
        return None

    @abstractmethod
    def is_valid(self, game: SequentialGame) -> bool:
        return not game.is_terminal()

    @abstractmethod
    def apply(self, game: SequentialGame) -> None:
        if not self.is_valid(game):
            raise InvalidActionException


class PlayerAction(Action, ABC):
    def is_valid(self, game: SequentialGame):
        return super().is_valid(game) and game.get_turn() is not None


class NatureAction(Action, ABC):
    def is_valid(self, game: SequentialGame):
        return super().is_valid(game) and game.get_turn() is None
