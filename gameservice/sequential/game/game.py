from __future__ import annotations

from typing import Type, List, Dict, Any, Optional, TYPE_CHECKING

from gameservice.exceptions import InvalidNumPlayersException, InvalidActionException, TerminalGameError, \
    NotTerminalGameError

if TYPE_CHECKING:
    from .player import Player
    from .environment import Environment
    from .logic import Logic


class SequentialGame:
    min_num_players: int
    max_num_players: int

    player_type: Type[Player]
    environment_type: Type[Environment]
    logic_type: Type[Logic]

    def __init__(self, num_players: int):
        """
        All members variables are read only

        :param num_players:
        """

        if not self.get_min_num_players() <= num_players <= self.get_max_num_players():
            raise InvalidNumPlayersException

        self._num_players: int = num_players

        self._players: List[Optional[Player]] = [self.create_player(i) for i in range(num_players)]
        self._environment: Environment = self.create_environment()
        self._logic: Logic = self.create_logic()

    """Public methods that can be overloaded"""

    def get_min_num_players(self) -> int:
        return self.min_num_players

    def get_max_num_players(self) -> int:
        return self.max_num_players

    def get_player_type(self) -> Type[Player]:
        return self.player_type

    def get_environment_type(self) -> Type[Environment]:
        return self.environment_type

    def get_logic_type(self) -> Type[Logic]:
        return self.logic_type

    def create_player(self, index: int) -> Player:
        return self.get_player_type()(index)

    def create_environment(self) -> Environment:
        return self.get_environment_type()()

    def create_logic(self) -> Logic:
        return self.get_logic_type()(self)

    """Public methods (read-only)"""

    def get_players(self):
        return self._players

    def get_environment(self):
        return self._environment

    def get_logic(self):
        return self._logic

    """Public methods"""

    def get_num_players(self) -> int:
        return self._num_players

    def get_num_remaining(self) -> int:
        return self._num_players - self._players.count(None)

    def is_remaining(self, index: int) -> bool:
        return self._players[index] is not None

    def get_remaining_indices(self) -> List[int]:
        return [i for i in range(self.get_num_players()) if self.is_remaining(i)]

    def get_player_info(self, index: int, show_private: bool) -> Optional[Dict[str, Any]]:
        return self._players[index].get_info(show_private) if self.is_remaining(index) else None

    def get_environment_info(self) -> Dict[str, Any]:
        return self._environment.get_info()

    def get_action_set_info(self) -> Dict[Optional[str], Optional[Dict[str, Any]]]:
        return {
            action_name: action_type.get_info(self) for action_name, action_type in self._logic.get_action_set().items()
        }

    def act(self, action_name: Optional[str] = None, *args) -> None:
        try:
            if self.is_terminal():
                raise TerminalGameError

            self._logic.get_action_set()[action_name](*args).apply(self)
        except (KeyError, TypeError):
            raise InvalidActionException

        self._logic.update()

    def get_turn(self) -> Optional[int]:
        if self.is_terminal():
            raise TerminalGameError

        return self._logic.get_turn()

    def is_terminal(self) -> bool:
        return self._logic.is_terminal()

    def get_result(self) -> List[int]:
        if not self.is_terminal():
            raise NotTerminalGameError

        return self._logic.get_result()
