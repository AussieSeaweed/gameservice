from typing import List, Optional, Sequence

from gameframe.game import Env, Nature, Player, Action
from gameframe.sequential import SequentialGame


class TicTacToeGame(SequentialGame['TicTacToeEnv', 'TicTacToeNature',
                                   'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe games."""

    def __init__(self):
        super().__init__(TicTacToeEnv(), TicTacToeNature(),
                         (TicTacToePlayer(self), TicTacToePlayer(self)), 0)


class TicTacToeEnv(Env):
    """TicTacToeEnv is the class for tic tac toe environments."""

    def __init__(self) -> None:
        self._board: List[List[Optional[TicTacToePlayer]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    @property
    def board(self) -> Sequence[Sequence[Optional['TicTacToePlayer']]]:
        """
        :return: the board of this tic tac toe environment
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_coordinates(self) -> Sequence[Sequence[int]]:
        """
        :return: the list of empty coordinates of the board
        """
        return [[r, c] for r in range(3) for c in range(3) if
                self.board[r][c] is None]

    @property
    def winner(self) -> Optional['TicTacToePlayer']:
        """
        :return: the winning player of the tic tac toe game if there is one, else None
        """
        for i in range(3):
            if self.board[i][0] is self.board[i][1] is self.board[i][2] is \
                    not None:
                return self.board[i][0]
            elif self.board[0][i] is self.board[1][i] is self.board[2][i] is \
                    not None:
                return self.board[0][i]

        if self.board[0][0] is self.board[1][1] is self.board[2][2] is not \
                None or self.board[0][2] is self.board[1][1] is \
                self.board[2][0] is not None:
            return self.board[1][1]

        return None


class TicTacToeNature(Nature):
    """TicTacToeNature is the class for tic tac toe natures."""

    @property
    def actions(self):
        return []


class TicTacToePlayer(Player):
    """TicTacToePlayer is the class for tic tac toe players."""

    def __init__(self, game: TicTacToeGame):
        super().__init__(game)

        self.__game = game

    @property
    def actions(self) -> List['MarkAction']:
        if self is self.__game.actor:
            return [MarkAction(self.__game, r, c) for r, c in
                    self.__game.env.empty_coordinates]
        else:
            return []

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        :raise: GameFrameException if the player cannot mark the cell
        """
        MarkAction(self.__game, r, c).act()


class MarkAction(Action):
    """MarkAction is the class for mark actions."""

    def __init__(self, game: TicTacToeGame, r: int, c: int):
        super().__init__(game)

        self.__game = game

        self.__r = r
        self.__c = c

    def __str__(self) -> str:
        return f'Mark row {self.r} column {self.c}'

    @property
    def r(self) -> int:
        """
        :return: the row number of this mark action
        """
        return self.__r

    @property
    def c(self) -> int:
        """
        :return: the column number of this mark action
        """
        return self.__c

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and not self.__game.actor.is_nature and \
               0 <= self.r < 3 and 0 <= self.c < 3 and \
               self.game.environment.board[self.r][self.c] is None

    @property
    def is_public(self):
        return True

    def act(self):
        super().act()

        self.game.environment._board[self.r][self.c] = self.actor

        if self.game.environment.empty_coordinates and self.game.environment.winner is None:
            self.game._actor = next(self.actor)
        else:
            self.game._actor = None
