from __future__ import annotations

from typing import Optional, Dict, Any, TYPE_CHECKING

from gameservice.exceptions import InvalidActionArgumentException
from ..game import Action

if TYPE_CHECKING:
    from .game import TicTacToe


class Mark(Action):
    def __init__(self, r: int, c: int, *args):
        super().__init__(*args)

        if not (isinstance(r, int) and isinstance(c, int) and 0 <= r < 3 and 0 <= c < 3):
            raise InvalidActionArgumentException

        self.r: int = r
        self.c: int = c

    @classmethod
    def info(cls, game: TicTacToe) -> Optional[Dict[str, Any]]:
        return {
            "empty_cell_coords": game.environment.empty_cell_coords,
            "winning_cell_coords": game.environment.winning_cell_coords,
        }

    def valid(self, game: TicTacToe) -> bool:
        return not game.terminal and game.turn is not None and [self.r, self.c] in game.environment.empty_cell_coords

    def apply(self, game: TicTacToe) -> None:
        super().apply(game)

        game.environment.board[self.r][self.c] = game.turn
