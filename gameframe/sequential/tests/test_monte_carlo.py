from abc import ABC
from typing import Generic

from gameframe.game.tests.test_monte_carlo import MCTestCaseMixin
from gameframe.sequential.generics import G


class SeqMCTestCaseMixin(MCTestCaseMixin[G], Generic[G], ABC):
    def verify(self, game: G) -> None:
        super().verify(game)

        if game.terminal:
            assert game.actor is None
        else:
            assert game.actor is not None
