from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Type, List, Dict, Any, Optional, TYPE_CHECKING

from gameservice.exceptions import InvalidNumPlayersException, InvalidActionException, TerminalError

if TYPE_CHECKING:
    from . import Action, Board, Player


class SequentialGame(ABC):
    min_num_players: int
    max_num_players: int

    player_type: Type[Player]
    board_type: Type[Board]
    action_set: Dict[str, Type[Action]]

    def __init__(self, num_players: int):
        if not self.min_num_players <= num_players <= self.max_num_players:
            raise InvalidNumPlayersException

        self.num_players: int = num_players

        self.players: List[Optional[Player]] = [self._create_player(i) for i in range(num_players)]
        self.board: Board = self._create_board()

    """Protected methods"""

    def _create_player(self, index: int) -> Player:
        return self.player_type(index)

    def _create_board(self) -> Board:
        return self.board_type()

    """Public methods"""

    @property
    def num_remaining(self) -> int:
        return self.num_players - self.players.count(None)

    def remaining(self, index: int) -> bool:
        return self.players[index] is not None

    def remaining_indices(self) -> List[int]:
        return [i for i in range(self.num_players) if self.remaining(i)]

    def player_info(self, index: int, show_private: bool) -> Dict[str, Any]:
        return self.players[index].info(show_private)

    @property
    def board_info(self) -> Dict[str, Any]:
        return self.board.info

    @property
    def action_set_info(self) -> Dict[str, Optional[Dict[str, Any]]]:
        return {
            action_str: action_type.info(self) for action_str, action_type in self.action_set.items()
        }

    def act(self, action_str: str, *args) -> None:
        try:
            if self.terminal:
                raise TerminalError

            self.action_set[action_str](*args).apply(self)
        except KeyError:
            raise InvalidActionException

    """Public abstract methods"""

    @property
    @abstractmethod
    def turn(self) -> Optional[int]:
        pass

    @property
    @abstractmethod
    def terminal(self) -> bool:
        pass
