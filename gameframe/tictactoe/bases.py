from __future__ import annotations

from typing import List, Optional, Sequence, Union

from gameframe.game import Action, Actor
from gameframe.sequential import SeqAction, SeqEnv, SeqGame
from gameframe.utils import next_player


class TTTEnv(SeqEnv):
    """TTTEnv is the class for tic tac toe environments."""

    def __init__(self, actor: Union[TTTNature, TTTPlayer]) -> None:
        super().__init__(actor)

        self._board: List[List[Optional[TTTPlayer]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    @property
    def board(self) -> Sequence[Sequence[Optional[TTTPlayer]]]:
        """
        :return: the board of this tic tac toe environment
        """
        return tuple(map(tuple, self._board))

    @property
    def empty_coords(self) -> Sequence[Sequence[int]]:
        """
        :return: the list of empty coordinates of the board
        """
        return [[r, c] for r in range(3) for c in range(3)
                if self.board[r][c] is None]

    @property
    def winner(self) -> Optional[TTTPlayer]:
        """
        :return: the winning player of the tic tac toe game if there is one,
        else None
        """
        for i in range(3):
            if self.board[i][0] is self.board[i][1] is self.board[i][2] \
                    is not None:
                return self.board[i][0]
            elif self.board[0][i] is self.board[1][i] is self.board[2][i] \
                    is not None:
                return self.board[0][i]

        if self.board[0][0] is self.board[1][1] is self.board[2][2] \
                is not None or self.board[0][2] is self.board[1][1] \
                is self.board[2][0] is not None:
            return self.board[1][1]

        return None


class TTTNature(Actor):
    """TTTNature is the class for tic tac toe natures."""

    @property
    def actions(self) -> Sequence[Action[TTTEnv, TTTNature, TTTPlayer,
                                         TTTNature]]:
        return []


class TTTPlayer(Actor):
    """TTTPlayer is the class for tic tac toe players."""

    def __init__(self, game: TTTGame):
        self.__game = game

    @property
    def actions(self) -> Sequence[MarkAction]:
        if self is self.__game.env.actor:
            return [MarkAction(self.__game, self, r, c)
                    for r, c in self.__game.env.empty_coords]
        else:
            return []

    def mark(self, r: int, c: int) -> None:
        """Marks the cell of the board at the coordinates.

        :param r: the row number of the cell
        :param c: the column number of the cell
        :return: None
        :raise: GameFrameException if the player cannot mark the cell
        """
        MarkAction(self.__game, self, r, c).act()


class TTTGame(SeqGame[TTTEnv, TTTNature, TTTPlayer]):
    """TTTGame is the class for tic tac toe games."""

    def __init__(self) -> None:
        players = (TTTPlayer(self), TTTPlayer(self))
        super().__init__(TTTEnv(players[0]), TTTNature(), players)


class MarkAction(SeqAction[TTTEnv, TTTNature, TTTPlayer, TTTPlayer]):
    """MarkAction is the class for mark actions."""

    def __init__(self, game: TTTGame, actor: TTTPlayer, r: int, c: int):
        super().__init__(game, actor)

        self.__r = r
        self.__c = c

    def __str__(self) -> str:
        return f'Mark ({self.__r}, {self.__c})'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable \
               and isinstance(self._game.env.actor, TTTPlayer) \
               and 0 <= self.__r < 3 and 0 <= self.__c < 3 \
               and self._game.env.board[self.__r][self.__c] is None

    @property
    def is_public(self) -> bool:
        return True

    def act(self) -> None:
        super().act()

        self._game.env._board[self.__r][self.__c] = self._actor

        if self._game.env.empty_coords and self._game.env.winner is None:
            self._game.env._actor = next_player(self._game, self._actor)
        else:
            self._game.env._actor = None
