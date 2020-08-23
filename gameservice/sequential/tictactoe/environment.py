from __future__ import annotations

from typing import List, Dict, Optional, Any, TYPE_CHECKING

from ..game import Environment

if TYPE_CHECKING:
    from .game import TicTacToe


class TicTacToeEnvironment(Environment):
    def __init__(self, game: TicTacToe):
        super().__init__(game)

        self.board: List[List[Optional[int]]] = [[None, None, None],
                                                 [None, None, None],
                                                 [None, None, None]]

    @property
    def empty_cell_coords(self) -> List[List[int]]:
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def winning_cell_coords(self) -> Optional[List[List[int]]]:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return [[i, 0], [i, 1], [i, 2]]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return [[0, i], [1, i], [2, i]]

        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return [[0, 0], [1, 1], [2, 2]]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return [[0, 2], [1, 1], [2, 0]]

        return None

    @property
    def info(self) -> Dict[str, Any]:
        return {
            **super().info,

            "board": self.board
        }
