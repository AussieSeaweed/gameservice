from abc import ABC, abstractmethod

from ..game.game import Game


class SequentialGame(Game, ABC):
    @property
    @abstractmethod
    def player(self):
        pass


class TurnAlternationGame(SequentialGame, ABC):
    """
    No nature/chance events
    """

    initial_turn = None

    def __init__(self):
        super().__init__()

        self.turn = self.initial_turn

    @property
    def terminal(self):
        return self.turn is None

    @property
    def player(self):
        return None if self.terminal else self.players[self.turn]

    def update(self):
        self.turn = (self.turn + 1) % len(self.players)


class TurnQueueGame(SequentialGame, ABC):
    initial_order = []

    def __init__(self):
        super().__init__()

        self.order = self.initial_order

    @property
    def terminal(self):
        return not self.order

    @property
    def player(self):
        return None if self.terminal else \
            (self.players.nature if self.order[0] is None else self.players[self.order[0]])

    def update(self):
        self.order.pop(0)
