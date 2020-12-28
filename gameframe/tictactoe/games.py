from typing import List, Optional

from .environments import TicTacToeEnvironment
from .players import TicTacToeNature, TicTacToePlayer
from ..sequential import SequentialGame


class TicTacToeGame(SequentialGame['TicTacToeGame', TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer]):
    """TicTacToeGame is the class for all tic tac toe games."""

    def _create_environment(self) -> TicTacToeEnvironment:
        return TicTacToeEnvironment(self)

    def _create_nature(self) -> TicTacToeNature:
        return TicTacToeNature(self)

    def _create_players(self) -> List[TicTacToePlayer]:
        return [TicTacToePlayer(self), TicTacToePlayer(self)]

    @property
    def _initial_player(self) -> Optional[TicTacToePlayer]:
        return self.players[0]
