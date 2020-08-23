from __future__ import annotations

from typing import Type, List, Dict, Any, Optional, TYPE_CHECKING

from gameservice.exceptions import InvalidNumPlayersException, InvalidActionException, TerminalGameError, \
    NotTerminalGameError

if TYPE_CHECKING:
    from . import Environment, Logic, Player


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

        if not self.min_num_players <= num_players <= self.max_num_players:
            raise InvalidNumPlayersException

        self.num_players: int = num_players

        self.players: List[Optional[Player]] = [self._create_player(i) for i in range(num_players)]
        self.environment: Environment = self._create_environment()
        self.logic: Logic = self._create_logic()

    """Protected methods"""

    def _create_player(self, index: int) -> Player:
        return self.player_type(self, index)

    def _create_environment(self) -> Environment:
        return self.environment_type(self)

    def _create_logic(self) -> Logic:
        return self.logic_type(self)

    """Public methods"""

    @property
    def num_remaining(self) -> int:
        return self.num_players - self.players.count(None)

    def remaining(self, index: int) -> bool:
        return self.players[index] is not None

    @property
    def remaining_indices(self) -> List[int]:
        return [i for i in range(self.num_players) if self.remaining(i)]

    def player_info(self, index: int, show_private: bool) -> Optional[Dict[str, Any]]:
        return self.players[index].info(show_private) if self.remaining(index) else None

    @property
    def environment_info(self) -> Dict[str, Any]:
        return self.environment.info

    @property
    def action_set_info(self) -> Dict[str, Optional[Dict[str, Any]]]:
        return {
            action_str: action_type.info(self) for action_str, action_type in self.logic.action_set.items()
        }

    def act(self, action_str: str, *args) -> None:
        try:
            if self.terminal:
                raise TerminalGameError

            self.logic.action_set[action_str](*args).apply(self)
        except (KeyError, TypeError):
            raise InvalidActionException

        self.logic.update()

    @property
    def turn(self) -> Optional[int]:
        if self.terminal:
            raise TerminalGameError

        return self.logic.turn

    @property
    def terminal(self) -> bool:
        return self.logic.terminal

    @property
    def result(self) -> List[int]:
        if not self.terminal:
            raise NotTerminalGameError

        return self.logic.result
