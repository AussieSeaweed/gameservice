from abc import ABC, abstractmethod
from typing import Generic
from unittest import TestCase

from gameframe.game import E, G, N, P


class GameTestCase(TestCase, Generic[G, E, N, P], ABC):
    """GameTestCase is the abstract base class for all game test cases."""

    @staticmethod
    @abstractmethod
    def _create_game() -> G:
        pass

    @staticmethod
    @abstractmethod
    def _verify(game: G) -> None:
        pass
