from __future__ import annotations

from enum import auto
from typing import Any, Optional, final

from auxiliary import OrderedEnum, default, get

from gameframe.exceptions import ActionException
from gameframe.game import Game, _Action


@final
class RockPaperScissorsPlayer:
    """RockPaperScissorsPlayer is the class for rock paper scissors players."""

    def __init__(self, game: RockPaperScissors) -> None:
        self.__game = game
        self._hand: Optional[RockPaperScissorsHand] = None

    @property
    def hand(self) -> Optional[RockPaperScissorsHand]:
        """
        :return: The hand of this rock paper scissors player.
        """
        return self._hand

    def throw(self, hand: RockPaperScissorsHand) -> None:
        """Throws the specified hand.

        :param hand: The hand to be thrown.
        :return: None.
        """
        _ThrowAction(self.__game, self, hand).act()

    def can_throw(self, hand: Optional[RockPaperScissorsHand] = None) -> bool:
        """Determines if this rock paper scissors player can throw a hand.

        :param hand: The hand to be thrown.
        :return: True if this rock paper scissors player can throw a hand, else False.
        """
        try:
            _ThrowAction(self.__game, self, default(hand, next(iter(RockPaperScissorsHand)))).verify()
        except ActionException:
            return False
        else:
            return True


@final
class RockPaperScissors(Game[None, RockPaperScissorsPlayer]):
    """RockPaperScissors is the class for rock paper scissors games."""

    def __init__(self) -> None:
        super().__init__(None, (RockPaperScissorsPlayer(self), RockPaperScissorsPlayer(self)))

    @property
    def winner(self) -> Optional[RockPaperScissorsPlayer]:
        """
        :return: The winning player of this rock paper scissors game if there is one, else None.
        """
        if self.terminal and self.players[0]._hand != self.players[1]._hand:
            return max(self.players, key=lambda player: get(player._hand))
        else:
            return None

    @property
    def terminal(self) -> bool:
        return all(player._hand is not None for player in self.players)


@final
class RockPaperScissorsHand(OrderedEnum):
    """RockPaperScissorsHand is the enum for rock paper scissors hands."""
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, RockPaperScissorsHand):
            return (self.index + 1) % 3 == other.index
        else:
            return NotImplemented


class _ThrowAction(_Action[RockPaperScissors, RockPaperScissorsPlayer]):
    def __init__(self, game: RockPaperScissors, actor: RockPaperScissorsPlayer, hand: RockPaperScissorsHand):
        super().__init__(game, actor)

        self.hand = hand

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.hand, RockPaperScissorsHand):
            raise TypeError('The hand must be of type Hand')
        elif self.actor._hand is not None:
            raise ActionException('The player has already played a hand')

    def apply(self) -> None:
        self.actor._hand = self.hand
