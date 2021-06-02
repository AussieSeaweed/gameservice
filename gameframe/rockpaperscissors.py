from __future__ import annotations

from enum import auto
from random import choice
from typing import Optional, final

from auxiliary import OrderedEnum, get

from gameframe.exceptions import GameFrameError
from gameframe.game import Actor, BaseActor, Game, _Action


@final
class RockPaperScissors(Game[BaseActor, 'RockPaperScissorsPlayer']):
    """RockPaperScissors is the class for rock paper scissors games."""

    def __init__(self) -> None:
        super().__init__(Actor(self), (RockPaperScissorsPlayer(self), RockPaperScissorsPlayer(self)))

    @property
    def winner(self) -> Optional[RockPaperScissorsPlayer]:
        """Determines the winner of this rock paper scissors game.

        :return: The winning player of this rock paper scissors game if there is one, else None.
        """
        if not self.terminal or self.players[0].hand == self.players[1].hand:
            return None
        else:
            return max(self.players, key=lambda player: get(player.hand))

    @property
    def terminal(self) -> bool:
        return self.players[0].hand is not None and self.players[1].hand is not None


@final
class RockPaperScissorsPlayer(Actor[RockPaperScissors]):
    """RockPaperScissorsPlayer is the class for rock paper scissors players.

    :param game: The game of this rock paper scissors actor.
    """

    def __init__(self, game: RockPaperScissors):
        super().__init__(game)

        self._hand: Optional[RockPaperScissorsHand] = None

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
        _ThrowAction(hand, self).act()

    def can_throw(self, hand: Optional[RockPaperScissorsHand] = None) -> bool:
        """Determines if this rock paper scissors player can throw a hand.

        :param hand: The optional hand to be thrown.
        :return: True if this rock paper scissors player can throw a hand, else False.
        """
        return _ThrowAction(hand, self).can_act()


@final
class RockPaperScissorsHand(OrderedEnum):
    """RockPaperScissorsHand is the enum class for rock paper scissors hands.

    The rock paper scissors hand can be compared to each other according to the rock paper scissors rules.
    """

    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def __lt__(self, other: RockPaperScissorsHand) -> bool:
        if isinstance(other, RockPaperScissorsHand):
            return (self.index + 1) % 3 == other.index
        else:
            return NotImplemented


class _ThrowAction(_Action[RockPaperScissors, RockPaperScissorsPlayer]):
    def __init__(self, hand: Optional[RockPaperScissorsHand], actor: RockPaperScissorsPlayer):
        super().__init__(actor)

        self.hand = hand

    def verify(self) -> None:
        super().verify()

        if self.actor.hand is not None:
            raise GameFrameError('The player must not have played a hand previously')

    def apply(self) -> None:
        super().apply()

        if self.hand is None:
            self.hand = choice(tuple(RockPaperScissorsHand))

        self.actor._hand = self.hand
