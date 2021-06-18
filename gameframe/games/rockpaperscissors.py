"""This module defines various components of rock paper scissors games."""
from enum import Enum
from functools import cached_property
from random import choice

from gameframe import Actor, Game, GameFrameError, _Action


class RockPaperScissorsGame(Game):
    """RockPaperScissorsGame is the class for rock paper scissors games."""

    def __init__(self):
        super().__init__(Actor(self), (RockPaperScissorsPlayer(self), RockPaperScissorsPlayer(self)))

    @property
    def winner(self):
        """Determines the winner of this rock paper scissors game.

        :return: The winning player of this rock paper scissors game if there is one, else None.
        """
        if not self.is_terminal() or self.players[0]._hand is self.players[1]._hand:
            return None
        else:
            return max(self.players, key=RockPaperScissorsPlayer.hand.fget)

    def is_terminal(self):
        return self.players[0]._hand is not None and self.players[1]._hand is not None


class RockPaperScissorsPlayer(Actor):
    """RockPaperScissorsPlayer is the class for rock paper scissors players.

    :param game: The game of this rock paper scissors actor.
    """

    def __init__(self, game):
        super().__init__(game)

        self._hand = None

    @property
    def hand(self):
        """Returns None if this rock paper scissors did not throw a hand, else the hand that this rock paper scissors
        player threw.

        :return: The hand of this rock paper scissors player.
        """
        return self._hand

    def throw(self, hand=None):
        """Throws the optionally specified hand.

        If the hand is not specified, a random rock paper scissors hand is thrown.

        :param hand: The optional hand to be thrown.
        :return: None.
        """
        _ThrowAction(hand, self).act()

    def can_throw(self, hand=None):
        """Determines if this rock paper scissors player can throw a hand.

        :param hand: The optional hand to be thrown.
        :return: True if this rock paper scissors player can throw a hand, else False.
        """
        return _ThrowAction(hand, self).can_act()


class RockPaperScissorsHand(Enum):
    """RockPaperScissorsHand is the enum class for rock paper scissors hands.

    The rock paper scissors hand can be compared to each other according to the rock paper scissors rules.
    """

    ROCK = 'Rock'
    '''The rock hand.'''
    PAPER = 'Paper'
    '''The paper hand.'''
    SCISSORS = 'Scissors'
    '''The scissors hand.'''

    @cached_property
    def _index(self):
        return tuple(RockPaperScissorsHand).index(self)

    def __lt__(self, other):
        if isinstance(other, RockPaperScissorsHand):
            return (self._index + 1) % 3 == other._index
        else:
            return NotImplemented


class _ThrowAction(_Action):
    def __init__(self, hand, actor):
        super().__init__(actor)

        self.hand = hand

    def verify(self):
        super().verify()

        if self.hand is not None and not isinstance(self.hand, RockPaperScissorsHand):
            raise GameFrameError('The hand to be thrown is not a valid rock paper scissors hand')
        elif self.actor._hand is not None:
            raise GameFrameError('The player must not have played a hand previously')

    def apply(self):
        if self.hand is None:
            self.hand = choice(tuple(RockPaperScissorsHand))

        self.actor._hand = self.hand
