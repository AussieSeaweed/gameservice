from abc import ABC
from typing import cast

from gameframe.game import ActionException
from gameframe.poker.bases import PokerAction, PokerGame, PokerPlayer
from gameframe.poker.stages import BettingStage, ShowdownStage


class BettingAction(PokerAction[PokerPlayer], ABC):
    @property
    def next_actor(self) -> PokerPlayer:
        actor = self.game.players[(self.actor.index + 1) % len(self.game.players)]

        while not actor._is_relevant and actor is not cast(BettingStage, self.game.env._stage).aggressor:
            actor = self.game.players[(actor.index + 1) % len(self.game.players)]

        return actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, BettingStage):
            raise ActionException('Not a betting round')


class FoldAction(BettingAction):
    def act(self) -> None:
        self.actor._muck()

    def verify(self) -> None:
        super().verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise ActionException('Folding is redundant')


class CheckCallAction(BettingAction):
    @property
    def amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self) -> None:
        self.actor._commitment += self.amount


class BetRaiseAction(BettingAction):
    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.amount = amount

    def act(self) -> None:
        stage = cast(BettingStage, self.game.env._stage)
        stage.aggressor = self.actor
        stage.max_delta = max(stage.max_delta, self.amount - max(player.bet for player in self.game.players))

        self.actor._commitment += self.amount - self.actor.bet

    def verify(self) -> None:
        super().verify()

        stage = cast(BettingStage, self.game.env._stage)

        if max(player._commitment for player in self.game.players) >= self.actor._total:
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
        actor = self.game.players[(self.actor.index + 1) % len(self.game.players)]

        while actor.is_mucked:
            actor = self.game.players[(actor.index + 1) % len(self.game.players)]

        return actor

    def act(self) -> None:
        for player in self.game.players:
            if player.is_shown and player.hand > self.actor.hand and player._commitment >= self.actor._commitment:
                self.actor._muck()
                break
        else:
            self.show = True

        if self.show:
            self.actor._show()

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, ShowdownStage):
            raise ActionException('Game not in showdown')
