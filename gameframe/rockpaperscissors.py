from __future__ import annotations

from enum import auto
from typing import Optional, final

from auxiliary import OrderedEnum

from gameframe.exceptions import GameFrameValueError
from gameframe.game import Game, Actor


@final
class RockPaperScissors(Game['RockPaperScissors', 'RockPaperScissorsNature', 'RockPaperScissorsPlayer']):
    """RockPaperScissors is the class for rock paper scissors games."""

    def __init__(self) -> None:
        self._nature = RockPaperScissorsNature(self)
        self._players = [RockPaperScissorsPlayer(self), RockPaperScissorsPlayer(self)]

    @property
    def winner(self) -> Optional[RockPaperScissorsPlayer]:
        """
        :return: The winning player of this rock paper scissors game if there is one, else None.
        """
        h0, h1 = (player.hand for player in self.players)

        if h0 is None or h1 is None or h0 == h1:
            return None
        elif h0 < h1:
            return self.players[1]
        else:
            return self.players[0]

    def is_terminal(self) -> bool:
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
        self._game = game
        self._hand: Optional[RockPaperScissorsHand] = None

    @property
    def hand(self) -> Optional[RockPaperScissorsHand]:
        """Returns the hand of this rock paper scissors player.

        :return: The hand of this rock paper scissors player.
        """
        return self._hand

    def play(self, hand: RockPaperScissorsHand) -> None:
        """Plays the specified hand.

        :param hand: The hand to be thrown.
        :return: None.
        """
        self._act()

        if self.hand is not None:
            raise GameFrameValueError('The player has already played a hand')

        self._hand = hand


@final
class RockPaperScissorsHand(OrderedEnum):
    """RockPaperScissorsHand is the enum for rock paper scissors hands."""

    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def __lt__(self, other: RockPaperScissorsHand) -> bool:
        if isinstance(other, RockPaperScissorsHand):
            return (self.index + 1) % 3 == other.index
        else:
            return NotImplemented
