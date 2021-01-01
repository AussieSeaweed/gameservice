from __future__ import annotations

from typing import Any, Optional

from gameframe.game import Action, Environment, Nature, Player
from gameframe.sequential import SequentialAction, SequentialGame


class TicTacToeGame(SequentialGame['TicTacToeGame', 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe games."""

    def _create_environment(self: TicTacToeGame) -> TicTacToeEnvironment:
        return TicTacToeEnvironment(self)

    def _create_nature(self: TicTacToeGame) -> TicTacToeNature:
        return TicTacToeNature(self)

    def _create_players(self: TicTacToeGame) -> list[TicTacToePlayer]:
        return [TicTacToePlayer(self), TicTacToePlayer(self)]

    @property
    def _initial_actor(self: TicTacToeGame) -> TicTacToePlayer:
        return self.players[0]


class TicTacToeEnvironment(Environment[TicTacToeGame, 'TicTacToeEnvironment', 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeGame is the class for tic tac toe environments."""

    def __init__(self: TicTacToeEnvironment, game: TicTacToeGame) -> None:
        super().__init__(game)

        self.__board: list[list[Optional[TicTacToePlayer]]] = [[None, None, None],
                                                               [None, None, None],
                                                               [None, None, None]]

    @property
    def board(self: TicTacToeEnvironment) -> list[list[Optional[TicTacToePlayer]]]:
        """
        :return: the board of the tic tac toe environment
        """
        return self.__board

    @property
    def _empty_coordinates(self: TicTacToeEnvironment) -> list[list[int]]:
        return [[r, c] for r in range(3) for c in range(3) if self.board[r][c] is None]

    @property
    def _winner(self: TicTacToeEnvironment) -> Optional[TicTacToePlayer]:
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
    def _information(self: TicTacToeEnvironment) -> dict[str, Any]:
        return {
            'board': self.board,
        }


class TicTacToeNature(Nature[TicTacToeGame, TicTacToeEnvironment, 'TicTacToeNature', 'TicTacToePlayer']):
    """TicTacToeNature is the class for tic tac toe natures."""

    @property
    def actions(self: TicTacToeNature) -> list[Action[TicTacToeGame, TicTacToeEnvironment, 'TicTacToeNature',
                                                      'TicTacToePlayer']]:
        return []

    @property
    def payoff(self: TicTacToeNature) -> int:
        return 0


class TicTacToePlayer(Player[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, 'TicTacToePlayer']):
    """TicTacToePlayer is the class for tic tac toe players."""

    @property
    def actions(self: TicTacToePlayer) -> list[MarkAction]:
        if self is self.game.actor:
            return [MarkAction(self, r, c) for r, c in self.game.environment._empty_coordinates]
        else:
            return []

    @property
    def payoff(self: TicTacToePlayer) -> int:
        if self.game.environment._winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self.game.environment._winner is self else -1


class MarkAction(SequentialAction[TicTacToeGame, TicTacToeEnvironment, TicTacToeNature, TicTacToePlayer]):
    """MarkAction is the class for mark actions."""

    def __init__(self: MarkAction, player: TicTacToePlayer, r: int, c: int) -> None:
        super().__init__(player)

        self.__r: int = r
        self.__c: int = c

    def act(self: MarkAction) -> None:
        super().act()

        self.game.environment.board[self.__r][self.__c] = self.actor

        if self.game.environment._empty_coordinates and self.game.environment._winner is None:
            self.game._actor = next(self.actor)
        else:
            self.game._actor = None

    @property
    def chance(self: MarkAction) -> bool:
        return False

    @property
    def public(self: MarkAction) -> bool:
        return True

    def __str__(self: MarkAction) -> str:
        return f'Mark row {self.__r} column {self.__c}'

    def _verify(self: MarkAction) -> None:
        super()._verify()

        if not (0 <= self.__r < 3 and 0 <= self.__c < 3):
            raise ValueError('The cell coordinates are out of range')
        elif self.game.environment.board[self.__r][self.__c] is not None:
            raise ValueError('The cell is already occupied')