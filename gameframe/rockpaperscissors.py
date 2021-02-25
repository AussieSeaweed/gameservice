from __future__ import annotations

from enum import unique
from typing import Any, Optional, cast, final

from auxiliary.enums import OrderedEnum

from gameframe.exceptions import ActionException
from gameframe.game import Game, _Action


@final
class RPSPlayer:
    """RPSPlayer is the class for rock paper scissors players."""

    def __init__(self, game: RPSGame) -> None:
        self.__game = game
        self._hand: Optional[RPSHand] = None

    @property
    def hand(self) -> Optional[RPSHand]:
        """
        :return: the hand of this rock paper scissors player.
        """
        return self._hand

    def throw(self, hand: RPSHand) -> None:
        """Throws the specified hand.

        :param hand: the hand to be thrown
        :return: None
        """
        _ThrowAction(self.__game, self, hand).act()

    def can_throw(self) -> bool:
        """Determines if this rock paper scissors player can throw a hand.

        :return: True if this rock paper scissors player can throw a hand, else False
        """
        try:
            _ThrowAction(self.__game, self, next(iter(RPSHand))).verify()
        except ActionException:
            return False
        else:
            return True


@final
class RPSGame(Game[None, RPSPlayer]):
    """RPSGame is the class for rock paper scissors games."""

    def __init__(self) -> None:
        super().__init__(None, (RPSPlayer(self), RPSPlayer(self)))

    @property
    def terminal(self) -> bool:
        return all(player.hand is not None for player in self.players)

    @property
    def winner(self) -> Optional[RPSPlayer]:
        """
        :return: the winning player of this rock paper scissors game if there is one, else None
        """
        if self.terminal and self.players[0].hand != self.players[1].hand:
            return max(self.players, key=lambda player: cast(RPSHand, player.hand))
        else:
            return None


@final
@unique
class RPSHand(OrderedEnum):
    """RPSHand is the enum for rock paper scissors hands."""
    ROCK = 'Rock'
    PAPER = 'Paper'
    SCISSORS = 'Scissors'

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, RPSHand):
            return (self.index + 1) % 3 == other.index
        else:
            return NotImplemented


class _ThrowAction(_Action[RPSGame, RPSPlayer]):
    def __init__(self, game: RPSGame, actor: RPSPlayer, hand: RPSHand):
        super().__init__(game, actor)

        self.hand = hand

    def apply(self) -> None:
        self.actor._hand = self.hand

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.hand, RPSHand):
            raise TypeError('The hand must be of type Hand')
        elif self.actor.hand is not None:
            raise ActionException('The player has already played a hand')
