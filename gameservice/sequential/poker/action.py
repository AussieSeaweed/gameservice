from __future__ import annotations

from typing import Optional, Dict, Any, TYPE_CHECKING

from gameservice.exceptions import InvalidActionArgumentException
from ..game.action import Action

if TYPE_CHECKING:
    from .game import Poker


class Put(Action):
    amount: int

    def valid(self, game: Poker) -> bool:
        return not game.terminal and game.turn is not None

    def apply(self, game: Poker) -> None:
        super().apply(game)


class NoLimitPut(Put):
    def __init__(self, amount: int, *args):
        super().__init__(*args)

        if not isinstance(amount, int):
            raise InvalidActionArgumentException

        self.amount: int = amount

    @classmethod
    def info(cls, game: Poker) -> Optional[Dict[str, Any]]:
        return {

        }


class Continue(Action):
    pass


class Surrender(Action):
    pass


class Peel(Action):
    pass


class Deal(Action):
    pass


class Showdown(Action):
    pass


class Distribute(Action):
    pass
