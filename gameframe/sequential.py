"""This module defines the base abstract classes for all elements of sequential games in GameFrame.

Sequential games have an extra attribute of actor. It denotes the current actor to act in the game.
If they are set to None, the sequential games will become terminal.

All elements of sequential games in GameFrame should inherit from the above classes.
"""
from abc import ABC

from gameframe.exceptions import GameFrameError
from gameframe.game import Game, _Action


class SequentialGame(Game, ABC):
    """SequentialGame is the base abstract class for all sequential games.

    In sequential games, only one actor can act at a time and is stored in the actor property. If a sequential game is
    terminal, its actor attribute must be set to None to denote such.

    :param initial_actor_index: The initial actor index. If it is None, the initial actor is set to the nature.
    :param nature: The nature of this game.
    :param players: The players of this game.
    """

    def __init__(self, initial_actor_index, nature, players):
        super().__init__(nature, players)

        self._actor = self.nature if initial_actor_index is None else self.players[initial_actor_index]

    @property
    def actor(self):
        """Returns the current actor of this sequential game.

        :return: None if this game is terminal, else the current actor of this sequential game.
        """
        return self._actor

    def is_terminal(self):
        return self.actor is None


class _SequentialAction(_Action, ABC):
    def verify(self):
        super().verify()

        if self.game.actor is not self.actor:
            raise GameFrameError('The actor must be in turn to act')
