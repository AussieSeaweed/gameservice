from abc import ABC, abstractmethod
from typing import Generic

from gameframe.game import E, G, N, P


class GameTestCaseMixin(Generic[G, E, N, P], ABC):
    """GameTestCaseMixin is the abstract base mixin for all game test cases."""

    @staticmethod
    @abstractmethod
    def _create_game() -> G:
        pass

    @staticmethod
    @abstractmethod
    def _verify(game: G) -> None:
        pass
