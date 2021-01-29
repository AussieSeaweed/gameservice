from abc import ABC
from typing import Sequence, Union

from gameframe.game import Game
from gameframe.game.bases import E, N, P


class SequentialGame(Game[E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the
    actor property. If a sequential game is terminal, its actor attribute must
    be set to None to denote such.
    """

    def __init__(self, env: E, nature: N, players: Sequence[P],
                 initial_actor_index: int):
        super().__init__(env, nature, players)

        if initial_actor_index is None:
            self._actor = nature
        else:
            self._actor = players[initial_actor_index]

    @property
    def actor(self) -> Union[N, P]:
        """
        :return: the actor of this sequential game
        """
        return self._actor

    @property
    def is_terminal(self) -> bool:
        return self.actor is None
