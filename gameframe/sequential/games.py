from abc import ABC

from gameframe.game import Game


class SequentialGame(Game, ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.
    """

    def __init__(self, environment, nature, players, initial_actor):
        super().__init__(environment, nature, players)

        self._actor = initial_actor

    @property
    def actor(self):
        """
        :return: the actor in turn to act of this sequential game
        """
        return self._actor

    @property
    def terminal(self):
        return self.actor is None

    @property
    def _information(self):
        return {
            **super()._information,
            'actor': self.actor,
        }
