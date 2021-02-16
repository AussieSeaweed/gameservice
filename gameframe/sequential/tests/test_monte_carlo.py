from abc import ABC

from gameframe.game.tests.test_monte_carlo import MCTestCaseMixin
from gameframe.sequential.generics import SG


class SeqMCTestCaseMixin(MCTestCaseMixin[SG], ABC):
    def verify(self, game: SG) -> None:
        super().verify(game)

        if game.terminal:
            assert game.actor is None
        else:
            assert game.actor is not None
