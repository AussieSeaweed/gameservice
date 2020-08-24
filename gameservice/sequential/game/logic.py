from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Dict, Type, Optional, TYPE_CHECKING

from gameservice.exceptions import TerminalGameError, NotTerminalGameError

if TYPE_CHECKING:
    from .game import SequentialGame
    from .action import Action


class Logic(ABC):
    action_set: Dict[Optional[str], Type[Action]]

    def __init__(self, game: SequentialGame):
        self.game: SequentialGame = game

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def get_turn(self) -> Optional[int]:
        if self.is_terminal():
            raise TerminalGameError

        return None

    @abstractmethod
    def is_terminal(self) -> bool:
        return True

    @abstractmethod
    def get_result(self) -> List[int]:
        if not self.is_terminal:
            raise NotTerminalGameError

        return [0 for i in range(self.game.get_num_players())]

    def get_action_set(self) -> Dict[str, Type[Action]]:
        return self.action_set


class TurnAlternationLogic(Logic, ABC):
    def __init__(self, game: SequentialGame):
        super().__init__(game)

        self._turn: int = self.get_initial_turn()

    def get_initial_turn(self) -> Optional[int]:
        return self.game.get_remaining_indices()[0]

    def update(self) -> None:
        self._turn = (self._turn + 1) % self.game.get_num_players()

        while not self.game.is_remaining(self._turn):
            self._turn = (self._turn + 1) % self.game.get_num_players()

    def get_turn(self) -> Optional[int]:
        return super().get_turn() or self._turn


class TurnQueueLogic(Logic, ABC):
    def __init__(self, game: SequentialGame):
        super().__init__(game)

        self._order: List[Optional[int]] = self.get_initial_order()

    def get_initial_order(self) -> List[Optional[int]]:
        return self.game.get_remaining_indices()

    def add_turn(self, index: int) -> None:
        self._order.append(index)

    def update(self) -> None:
        try:
            self._order.pop(0)
        except IndexError:
            pass

    def get_turn(self) -> Optional[int]:
        return super().get_turn() or (self._order[0] if self._order else None)


class NestedLogic(Logic, ABC):
    nested_logic_types: List[Type[Logic]]

    def __init__(self, game: SequentialGame):
        super().__init__(game)

        self._nested_logics: List[Logic] = [nested_logic_type(game) for nested_logic_type in self.nested_logic_types]
        self._nested_logic_index: int = 0

        self._result: List[int] = [0 for i in range(game.get_num_players())]

    def update(self) -> None:
        self.get_nested_logic().update()

        if self.get_nested_logic().is_terminal():
            self._result = [i + j for i, j in zip(self._result, self.get_nested_logic().get_result())]
            self._nested_logic_index += 1

    def get_turn(self) -> Optional[int]:
        return super().get_turn() or self.get_nested_logic().get_turn()

    def is_terminal(self) -> bool:
        return self._nested_logic_index == len(self._nested_logics)

    def get_result(self) -> List[int]:
        return [i + j for i, j in zip(super().get_result(), self._result)]

    def get_action_set(self) -> Dict[Optional[str], Type[Action]]:
        return self.get_nested_logic().get_action_set()

    def get_nested_logic(self) -> Logic:
        return self._nested_logics[self._nested_logic_index]
