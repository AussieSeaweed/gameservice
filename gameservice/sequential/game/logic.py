from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Dict, Type, Optional, TYPE_CHECKING

from gameservice.exceptions import TerminalGameError, NotTerminalGameError

if TYPE_CHECKING:
    from gameservice.sequential.game.game import SequentialGame
    from .action import Action


class Logic(ABC):
    action_set: Dict[str, Type[Action]]

    def __init__(self, game: SequentialGame):
        self.game: SequentialGame = game

    @abstractmethod
    def update(self) -> None:
        pass

    @property
    @abstractmethod
    def turn(self) -> Optional[int]:
        if self.terminal:
            raise TerminalGameError

        return None

    @property
    @abstractmethod
    def terminal(self) -> bool:
        pass

    @property
    @abstractmethod
    def result(self) -> List[int]:
        if not self.terminal:
            raise NotTerminalGameError

        return []


class TurnAlternationLogic(Logic, ABC):
    def __init__(self, game: SequentialGame):
        super().__init__(game)
        self._turn: int = self._initial_turn

    @property
    def _initial_turn(self) -> Optional[int]:
        return self.game.remaining_indices[0]

    def update(self) -> None:
        self._turn = (self._turn + 1) % self.game.num_players

        while not self.game.remaining(self._turn):
            self._turn = (self._turn + 1) % self.game.num_players

    @property
    def turn(self) -> Optional[int]:
        return super().turn or self._turn


class TurnQueueLogic(Logic, ABC):
    def __init__(self, game: SequentialGame):
        super().__init__(game)
        self._order: List[Optional[int]] = self._initial_order

    @property
    def _initial_order(self) -> List[Optional[int]]:
        return self.game.remaining_indices

    def add_turn(self, index: int) -> None:
        self._order.append(index)

    def update(self) -> None:
        try:
            self._order.pop(0)
        except IndexError:
            pass

    @property
    def turn(self) -> Optional[int]:
        return super().turn or (self._order[0] if self._order else None)
