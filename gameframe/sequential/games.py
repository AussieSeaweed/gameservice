from abc import ABC, abstractmethod
from typing import Dict, Optional

from .utils import G
from ..game import E, Game, N, P


class SequentialGame(Game[G, E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one player can act at a time. The player in turn can be accessed through the player
    attribute of the SequentialGame instance. The initial_player abstract property should be overridden by the
    subclasses to represent the player who is the first to act. If a sequential game is terminal, its player attribute
    must be set to None to denote such.
    """

    def __init__(self):
        super().__init__()

        self.player: P = self._initial_player

    @property
    def terminal(self) -> bool:
        return self.player is None

    @property
    def _information(self) -> Dict[str, str]:
        return {
            **super()._information,
            'player': self.player,
        }

    @property
    @abstractmethod
    def _initial_player(self) -> Optional[P]:
        pass
