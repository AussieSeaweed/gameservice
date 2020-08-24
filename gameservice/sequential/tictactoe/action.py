from __future__ import annotations

from typing import Optional, Dict, Any, TYPE_CHECKING

from gameservice.exceptions import InvalidActionArgumentException
from ..game.action import PlayerAction

if TYPE_CHECKING:
    from .game import TicTacToe


class Mark(PlayerAction):
    def __init__(self, r: int, c: int, *args):
        super().__init__(*args)

        if not (isinstance(r, int) and isinstance(c, int) and 0 <= r < 3 and 0 <= c < 3):
            raise InvalidActionArgumentException

        self.r: int = r
        self.c: int = c

    @classmethod
    def get_info(cls, game: TicTacToe) -> Optional[Dict[str, Any]]:
        return {
            "empty_cell_coords": game.get_environment().get_empty_cell_coords(),
        }

    def is_valid(self, game: TicTacToe) -> bool:
        return super().is_valid(game) and [self.r, self.c] in game.get_environment().get_empty_cell_coords()

    def apply(self, game: TicTacToe) -> None:
        super().apply(game)

        game.get_environment().board[self.r][self.c] = game.get_turn()
