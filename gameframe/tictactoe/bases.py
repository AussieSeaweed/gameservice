from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from gameframe.game import Environment, Nature, Player
from gameframe.sequential import SequentialAction, SequentialGame


class TicTacToeGame(SequentialGame['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe games."""

    @property
    def _initial_actor(self) -> TicTacToePlayer:
        return self.players[0]

    def _create_environment(self) -> TicTacToeEnvironment:
        return TicTacToeEnvironment(self)

    def _create_nature(self) -> TicTacToeNature:
        return TicTacToeNature(self)

    def _create_players(self) -> list[TicTacToePlayer]:
        return [TicTacToePlayer(self), TicTacToePlayer(self)]


class TicTacToeEnvironment(Environment[TicTacToeGame, 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe environments."""

    def __init__(self, game: TicTacToeGame) -> None:
        super().__init__(game)

        self.__board: list[list[Optional[TicTacToePlayer]]] = [[None, None, None],
                                                               [None, None, None],
                                                               [None, None, None]]

    @property
    def board(self) -> list[list[Optional[TicTacToePlayer]]]:
        """
        :return: the board of the tic tac toe environment
        """
        return self.__board

    @property
    def _empty_coordinates(self) -> list[list[int]]:
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def _information(self) -> dict[str, Any]:
        return {
            'board': self.board,
        }

    @property
    def _winner(self) -> Optional[TicTacToePlayer]:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                return self.board[i][0]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None or \
                self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
            return self.board[1][1]

        return None


class TicTacToeNature(Nature[TicTacToeGame, TicTacToeEnvironment, 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeNature is the class for tic tac toe natures."""

    @property
    def actions(self) -> list[TicTacToeAction]:
        return []

    @property
    def payoff(self) -> int:
        return 0


class TicTacToePlayer(Player[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, 'TicTacToePlayer']):
    """TicTacToePlayer is the class for tic tac toe players."""

    @property
    def actions(self) -> list[TicTacToeAction]:
        from gameframe.tictactoe import MarkAction

        if self is self.game.actor:
            return [MarkAction(self, r, c) for r, c in self.game.environment._empty_coordinates]
        else:
            return []

    @property
    def payoff(self) -> int:
        if self.game.environment._winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self is self.game.environment._winner else -1


class TicTacToeAction(SequentialAction[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer], ABC):
    """TicTacToeAction is the abstract base class for all tic tac toe actions"""

    @property
    def chance(self) -> bool:
        return False

    @property
    def public(self) -> bool:
        return True
