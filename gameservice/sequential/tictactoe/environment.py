from __future__ import annotations

from typing import List, Dict, Optional, Any

from ..game.environment import Environment


class TicTacToeEnvironment(Environment):
    def __init__(self):
        self.board: List[List[Optional[int]]] = [[None, None, None],
                                                 [None, None, None],
                                                 [None, None, None]]

    def get_empty_cell_coords(self) -> List[List[int]]:
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    def get_winning_cell_coords(self) -> Optional[List[List[int]]]:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return [[i, 0], [i, 1], [i, 2]]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return [[0, i], [1, i], [2, i]]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
            return [[0, 0], [1, 1], [2, 2]]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return [[0, 2], [1, 1], [2, 0]]

        return None

    def get_info(self) -> Dict[str, Any]:
        return {
            "board": self.board
        }
