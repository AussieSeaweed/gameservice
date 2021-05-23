from __future__ import annotations

from enum import auto
from random import choice
from typing import Optional, final

from auxiliary import OrderedEnum, default

from gameframe.exceptions import GameFrameValueError
from gameframe.game import Actor, Game, _Action


@final
class RockPaperScissors(Game['RockPaperScissors', 'RockPaperScissorsNature', 'RockPaperScissorsPlayer']):
    """RockPaperScissors is the class for rock paper scissors games."""

    def __init__(self) -> None:
        self._nature = RockPaperScissorsNature(self)
        self._players = [RockPaperScissorsPlayer(self), RockPaperScissorsPlayer(self)]

    @property
    def winner(self) -> Optional[RockPaperScissorsPlayer]:
        """Determines the winner of this rock paper scissors game.

        :return: The winning player of this rock paper scissors game if there is one, else None.
        """
        h0, h1 = (player.hand for player in self.players)

        if h0 is None or h1 is None or h0 == h1:
            return None
        elif h0 < h1:
            return self.players[1]
        else:
            return self.players[0]

    @property
    def terminal(self) -> bool:
        return self.players[0].hand is not None and self.players[1].hand is not None


@final
class RockPaperScissorsNature(Actor[RockPaperScissors, 'RockPaperScissorsNature', 'RockPaperScissorsPlayer']):
    """RockPaperScissorsNature is the class for rock paper scissors natures."""

    def __init__(self, game: RockPaperScissors):
        self._game = game


@final
class RockPaperScissorsPlayer(Actor[RockPaperScissors, RockPaperScissorsNature, 'RockPaperScissorsPlayer']):
    """RockPaperScissorsPlayer is the class for rock paper scissors players."""

    def __init__(self, game: RockPaperScissors):
        self._hand: Optional[RockPaperScissorsHand] = None
        self._game = game

    @property
    def hand(self) -> Optional[RockPaperScissorsHand]:
        """Returns the hand of this rock paper scissors player.

        :return: The hand of this rock paper scissors player.
        """
        return self._hand

    def throw(self, hand: Optional[RockPaperScissorsHand] = None) -> None:
        """Throws the optionally specified hand.

        If the hand is not specified, a random rock paper scissors hand is thrown.

        :param hand: The optional hand to be thrown.
        :return: None.
        """
        _ThrowAction(self, hand).act()

    def can_throw(self, hand: Optional[RockPaperScissorsHand] = None) -> bool:
        """Determines if this rock paper scissors player can throw a hand.

        :param hand: The optional hand to be thrown.
        :return: True if this rock paper scissors player can throw a hand, else False.
        """
        return _ThrowAction(self, hand).can_act()


@final
class RockPaperScissorsHand(OrderedEnum):
    """RockPaperScissorsHand is the enum class for rock paper scissors hands."""

    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def __lt__(self, other: RockPaperScissorsHand) -> bool:
        if isinstance(other, RockPaperScissorsHand):
            return (self.index + 1) % 3 == other.index
        else:
            return NotImplemented


class _ThrowAction(_Action[RockPaperScissorsPlayer]):
    def __init__(self, actor: RockPaperScissorsPlayer, hand: Optional[RockPaperScissorsHand] = None):
        self.hand = hand
        self.actor = actor

    def verify(self) -> None:
        super().verify()

        if self.actor.hand is not None:
            raise GameFrameValueError('The player must not have played a hand previously')

    def apply(self) -> None:
        self.actor._hand = default(self.hand, choice(tuple(RockPaperScissorsHand)))
