from __future__ import annotations

from typing import List, TYPE_CHECKING

from gameservice.exceptions import NotTerminalGameError
from ..game import TurnAlternationLogic
from .action import Mark

if TYPE_CHECKING:
    from .game import TicTacToe


class TicTacToeLogic(TurnAlternationLogic):
    action_set = {
        "mark": Mark
    }

    """Type hinting"""

    game: TicTacToe

    def __init__(self, game: TicTacToe):
        super().__init__(game)

    @property
    def terminal(self) -> bool:
        return self.game.environment.winning_cell_coords is not None or not self.game.environment.empty_cell_coords

    @property
    def result(self) -> List[int]:
        return super().result or ([0, 0] if self.winner is None else [1 - 2 * self.winner, 2 * self.winner - 1])

    @property
    def winner(self):
        if not self.terminal:
            raise NotTerminalGameError

        try:
            r, c = self.game.environment.winning_cell_coords[0]

            return self.game.environment.board[r][c]
        except ValueError:
            return None
