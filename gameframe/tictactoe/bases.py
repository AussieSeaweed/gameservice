from __future__ import annotations

from abc import ABC
from collections.abc import Mapping, MutableSequence, Sequence
from typing import Any, Optional, Union, final

from gameframe.game import Actor, Environment
from gameframe.sequential import SequentialAction, SequentialGame
from gameframe.utils import override

__all__ = ['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer', 'TicTacToeAction']


@final
class TicTacToeGame(SequentialGame['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        super().__init__(TicTacToeEnvironment(self), TicTacToeNature(self),
                         (TicTacToePlayer(self), TicTacToePlayer(self)), 0)


@final
class TicTacToeEnvironment(Environment[TicTacToeGame, 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe environments."""

    def __init__(self, game: TicTacToeGame) -> None:
        super().__init__(game)

        self._board: MutableSequence[MutableSequence[Optional[TicTacToePlayer]]] = [[None, None, None],
                                                                                    [None, None, None],
                                                                                    [None, None, None]]

    @property
    def board(self) -> Sequence[Sequence[Optional[TicTacToePlayer]]]:
        """
        :return: the board of the tic tac toe environment
        """
        return self._board

    @property
    def _empty_coordinates(self) -> Sequence[Sequence[int]]:
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

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

    @property
    @override
    def _information(self) -> Mapping[str, Any]:
        return {
            'board': self.board,
        }


@final
class TicTacToeNature(Actor[TicTacToeGame, TicTacToeEnvironment, 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeNature is the class for tic tac toe natures."""

    @property
    @override
    def actions(self) -> Sequence[TicTacToeAction]:
        return []

    @property
    @override
    def payoff(self) -> int:
        return 0


@final
class TicTacToePlayer(Actor[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, 'TicTacToePlayer']):
    """TicTacToePlayer is the class for tic tac toe players."""

    @property
    @override
    def actions(self) -> Sequence[TicTacToeAction]:
        from gameframe.tictactoe import MarkAction

        if self is self.game.actor:
            return [MarkAction(self, r, c) for r, c in self.game.environment._empty_coordinates]
        else:
            return []

    @property
    @override
    def payoff(self) -> int:
        if self.game.environment._winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self is self.game.environment._winner else -1


class TicTacToeAction(SequentialAction[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer], ABC):
    """TicTacToeAction is the abstract base class for all tic tac toe actions"""

    def __init__(self, actor: Union[TicTacToeNature, TicTacToePlayer]) -> None:
        super().__init__(actor, False, True)
