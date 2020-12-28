from __future__ import annotations

from typing import List, TYPE_CHECKING

from .actions import MarkAction
from ..game import Player

if TYPE_CHECKING:
    from ..game import Action
    from . import TicTacToeGame, TicTacToeEnvironment


class TicTacToePlayer(Player['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToePlayer is the class for tic tac toe players."""

    @property
    def actions(self) -> List[Action[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer]]:
        if self is self.game.player:
            return [MarkAction(self, r, c) for r, c in self.game.environment._empty_coordinates]
        else:
            return []

    @property
    def payoff(self) -> int:
        if self.game.environment._winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self.game.environment._winner is self else -1


class TicTacToeNature(Player['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', TicTacToePlayer]):
    """TicTacToeNature is the class for all tic tac toe natures."""

    @property
    def actions(self) -> List[Action[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer]]:
        return []

    @property
    def payoff(self) -> int:
        return 0
