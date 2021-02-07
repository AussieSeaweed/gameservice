from __future__ import annotations

from enum import Enum, unique
from typing import Any, Optional

from gameframe.game import ActionException
from gameframe.game.generics import Action, Actor, Game


class RPSGame(Game[Actor['RPSGame'], 'RPSPlayer']):
    """RPSGame is the class for rock paper scissors games."""

    def __init__(self) -> None:
        nature = Actor(self)
        players = RPSPlayer(self), RPSPlayer(self)

        super().__init__(nature, players)

    @property
    def winner(self) -> Optional[RPSPlayer]:
        """
        :return: the winning player of the rock paper scissors game if there is one, else None
        """
        if self.players[0].hand is not None and self.players[1].hand is not None \
                and self.players[0].hand != self.players[1].hand:
            return self.players[0] if self.players[0].hand > self.players[1].hand else self.players[1]
        else:
            return None

    @property
    def terminal(self) -> bool:
        return all(player.hand is not None for player in self.players)


class RPSPlayer(Actor[RPSGame]):
    """RPSPlayer is the class for rock paper scissors players."""

    def __init__(self, game: RPSGame) -> None:
        super().__init__(game)

        self._hand: Optional[Hand] = None

    @property
    def hand(self) -> Optional[Hand]:
        """
        :return: the hand of this rock paper scissors player.
        """
        return self._hand

    def throw(self, hand: Hand) -> None:
        """Throws the specified hand.

        :param hand: the hand to be thrown
        :return: None
        """
        ThrowAction(self.game, self, hand).act()


class ThrowAction(Action[RPSGame, RPSPlayer]):
    def __init__(self, game: RPSGame, actor: RPSPlayer, hand: Hand):
        super().__init__(game, actor)

        self.hand = hand

    def apply(self) -> None:
        self.actor._hand = self.hand

    def verify(self) -> None:
        super().verify()

        if self.actor.hand is not None:
            raise ActionException('The player has already played a hand')


@unique
class Hand(Enum):
    """Hand is the enum for rock paper scissors hands."""
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Hand):
            return (self.value + 1) % 3 == other.value
        else:
            return NotImplemented
