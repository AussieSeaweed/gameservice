from __future__ import annotations

from typing import List, TYPE_CHECKING

from gameservice.exceptions import NotTerminalGameError
from .action import Mark
from ..game.logic import TurnAlternationLogic

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

    def is_terminal(self) -> bool:
        return self.game.get_environment().get_winning_cell_coords() is not None or \
               not self.game.get_environment().get_empty_cell_coords()

    def get_result(self) -> List[int]:
        return [i + j for i, j in zip(super().get_result(), ([0, 0] if self.get_winner() is None else
                                                             [1 - 2 * self.get_winner(), 2 * self.get_winner() - 1]))]

    def get_winner(self):
        if not self.is_terminal():
            raise NotTerminalGameError

        try:
            r, c = self.game.get_environment().get_winning_cell_coords()[0]

            return self.game.get_environment().board[r][c]
        except TypeError:
            return None
