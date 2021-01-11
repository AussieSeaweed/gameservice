from abc import ABC

from gameframe.game import Game


class SequentialGame(Game, ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    def __init__(self, environment, nature, players, initial_actor_index):
        super().__init__(environment, nature, players)

        self.actor = nature if initial_actor_index is None else players[initial_actor_index]

    @property
    def information(self):
        return {
            **super().information,
            'actor': self.actor,
        }

    @property
    def is_terminal(self):
        return self.actor is None
