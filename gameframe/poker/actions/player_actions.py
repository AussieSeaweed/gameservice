from abc import ABC
from typing import cast

from gameframe.game import ActionException
from gameframe.poker.bases import PokerAction, PokerGame, PokerPlayer
from gameframe.poker.stages import BettingStage, ShowdownStage


class BettingAction(PokerAction[PokerPlayer], ABC):
    @property
    def next_actor(self) -> PokerPlayer:
        actor = next(self.actor)

        while not actor._is_relevant and actor is not self.game._aggressor:
            actor = next(actor)

        return actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, BettingStage):
            raise ActionException('Not a betting round')


class FoldAction(BettingAction):
    def apply(self) -> None:
        self.actor._status = PokerPlayer.HoleCardStatus.MUCKED

    def verify(self) -> None:
        super().verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise ActionException('Folding is redundant')


class CheckCallAction(BettingAction):
    @property
    def amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def apply(self) -> None:
        self.actor._commitment += self.amount


class BetRaiseAction(BettingAction):
    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.amount = amount

    def apply(self) -> None:
        cast(BettingStage, self.game._stage).flag = BettingStage.Flag.DEFAULT

        self.game._aggressor = self.actor
        self.game._max_delta = max(self.game._max_delta, self.amount - max(player.bet for player in self.game.players))

        self.actor._commitment += self.amount - self.actor.bet

    def verify(self) -> None:
        super().verify()

        stage = cast(BettingStage, self.game._stage)

        if max(player._commitment for player in self.game.players) >= self.actor.starting_stack:
            raise ActionException('The stack of the acting player is covered')
        elif all(not player._is_relevant for player in self.game.players if player is not self.actor):
            raise ActionException('Betting/Raising is redundant')
        elif not stage.min_amount <= self.amount <= stage.max_amount:
            raise ActionException('The bet/raise amount is not allowed')


class ShowdownAction(PokerAction[PokerPlayer]):
    def __init__(self, game: PokerGame, actor: PokerPlayer, show: bool):
        super().__init__(game, actor)

        self.show = show

    @property
    def next_actor(self) -> PokerPlayer:
        actor = next(self.actor)

        while actor.is_mucked:
            actor = next(actor)

        return actor

    def apply(self) -> None:
        if self.show or all(not (player.hand > self.actor.hand and player._commitment >= self.actor._commitment)
                            for player in self.game.players if player.is_shown):
            self.actor._status = PokerPlayer.HoleCardStatus.SHOWN
        else:
            self.actor._status = PokerPlayer.HoleCardStatus.MUCKED

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, ShowdownStage):
            raise ActionException('Game not in showdown')
