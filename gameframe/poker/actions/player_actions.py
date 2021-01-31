from abc import ABC
from typing import cast

from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.stages import BettingStage, DistributionStage, ShowdownStage
from gameframe.utils import rotate


class BettingAction(PokerAction[PokerPlayer], ABC):
    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, BettingStage):
            raise ValueError('Not a betting round')


class FoldAction(BettingAction):
    def act(self) -> None:
        super().act()

        self.actor._muck()

        if sum(not player.is_mucked for player in self.game.players) == 1:
            self.change_stage(DistributionStage(self.game))
        else:
            self.game.env._actor = next(self.actor)

            if isinstance(self.game.env.actor, PokerNature):
                self.change_stage()

    def verify(self) -> None:
        super().verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise ValueError('Folding is redundant')


class CheckCallAction(BettingAction):
    @property
    def amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self) -> None:
        super().act()

        self.actor._commitment += self.amount
        self.game.env._actor = next(self.actor)

        if isinstance(self.game.env.actor, PokerNature):
            self.change_stage()


class BetRaiseAction(BettingAction):
    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.amount = amount

    def act(self) -> None:
        super().act()

        self.game.env._aggressor = self.actor
        self.game.env._max_delta = max(self.game.env._max_delta,
                                       self.amount - max(player.bet for player in self.game.players))

        self.actor._commitment += self.amount - self.actor.bet
        self.game.env._actor = next(self.actor)

    def verify(self) -> None:
        super().verify()

        stage = cast(BettingStage, self.game.env._stage)

        if max(player._commitment for player in self.game.players) >= self.actor._total:
            raise ValueError('The stack of the acting player is covered')
        elif all(not player._is_relevant for player in self.game.players if player is not self.actor):
            raise ValueError('Betting/Raising is redundant')
        elif not stage.min_amount <= self.amount <= stage.max_amount:
            raise ValueError('The bet/raise amount is not allowed')


class ShowdownAction(PokerAction[PokerPlayer]):
    def __init__(self, game: PokerGame, actor: PokerPlayer, show: bool):
        super().__init__(game, actor)

        self.show = show

    def act(self) -> None:
        index = 0 if self.game.env._aggressor is None else self.game.env._aggressor.index
        players = [player for player in rotate(self.game.players, index) if not player.is_mucked]

        for player in players[:players.index(self.actor)]:
            if player.hand < self.actor.hand and player._commitment >= self.actor._commitment:
                player._muck()
                break
        else:
            self.show = True

        if self.show:
            for card in self.actor._hole_cards:
                card._status = True

        if players[-1] is self.actor:
            self.change_stage()
        else:
            self.game.env._actor = players[players.index(self.actor) + 1]

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, ShowdownStage):
            raise ValueError('Game not in showdown')
