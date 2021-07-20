"""This module defines various components of rock paper scissors games."""
from random import choice

from auxiliary import IndexedEnum, maxima, minima

from gameframe.exceptions import GameFrameError
from gameframe.game import Actor, Game, _Action


class RockPaperScissorsGame(Game):
    """RockPaperScissorsGame is the class for rock paper scissors games."""

    def __init__(self, player_count=2):
        if player_count < 2:
            raise ValueError('Rock paper scissors games require 2 or more players')

        super().__init__(Actor(self), (RockPaperScissorsPlayer(self) for _ in range(player_count)))

    @property
    def winners(self):
        """Determines the winner of this rock paper scissors game.

        :return: The winning players if this game is terminal, else None.
        """
        if not self.is_terminal():
            return None
        elif len(set(map(RockPaperScissorsPlayer.hand.fget, self.players))) in (1, 3):
            return iter(())
        else:
            return maxima(self.players, key=RockPaperScissorsPlayer.hand.fget)

    @property
    def losers(self):
        """Determines the losers of this rock paper scissors game.

        :return: The losing players if this game is terminal, else None.
        """
        if not self.is_terminal():
            return None
        elif len(set(map(RockPaperScissorsPlayer.hand.fget, self.players))) in (1, 3):
            return iter(())
        else:
            return minima(self.players, key=RockPaperScissorsPlayer.hand.fget)

    def throw(self, *hands):
        """Throws the given hands.

        :param hands: The hands to throw.
        :return: This game.
        """
        for player, hand in zip(self.players, hands):
            player.throw(hand)

        return self

    def is_terminal(self):
        return all(map(RockPaperScissorsPlayer.hand.fget, self.players))


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


class RockPaperScissorsHand(IndexedEnum):
    """RockPaperScissorsHand is the enum class for rock paper scissors hands.

    The rock paper scissors hand can be compared to each other according to the rock paper scissors rules.
    """

    ROCK = 'Rock'
    '''The rock hand.'''
    PAPER = 'Paper'
    '''The paper hand.'''
    SCISSORS = 'Scissors'
    '''The scissors hand.'''

    def __lt__(self, other):
        if isinstance(other, RockPaperScissorsHand):
            return (self.index + 1) % 3 == other.index
        else:
            return NotImplemented


class _ThrowAction(_Action):
    def __init__(self, hand, actor):
        super().__init__(actor)

        self.hand = hand

    def verify(self):
        super().verify()

        if self.hand is not None:
            if not isinstance(self.hand, RockPaperScissorsHand):
                raise TypeError('The hand to be thrown must be of type RockPaperScissorsHand')

        if self.actor.hand is not None:
            raise GameFrameError('The player must not have played a hand previously')

    def apply(self):
        self.actor._hand = choice(tuple(RockPaperScissorsHand)) if self.hand is None else self.hand
