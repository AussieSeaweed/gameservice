from abc import ABC

from gameframe.game import ActionException
from gameframe.poker.bases import PokerAction, PokerGame, PokerPlayer
from gameframe.poker.stages import BettingStage, ShowdownStage


class BettingAction(PokerAction[PokerPlayer, BettingStage], ABC):
    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, BettingStage):
            raise ActionException('Not a betting round')


class FoldAction(BettingAction):
    def act(self) -> None:
        super().act()

        self.actor._muck()

        if sum(not player.is_mucked for player in self.game.players) == 1:  # TODO: TRY WITHOUT
            self.change_stage()
        else:
            self.game.env._actor = next(self.actor)

            if self.game.env.actor is self.stage.aggressor:
                self.change_stage()

    def verify(self) -> None:
        super().verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise ActionException('Folding is redundant')


class CheckCallAction(BettingAction):
    @property
    def amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self) -> None:
        super().act()

        self.actor._commitment += self.amount
        self.game.env._actor = next(self.actor)

        if self.game.env.actor is self.stage.aggressor:
            self.change_stage()


class BetRaiseAction(BettingAction):
    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.amount = amount

    def act(self) -> None:
        super().act()

        self.stage.aggressor = self.actor
        self.stage.max_delta = max(self.stage.max_delta,
                                   self.amount - max(player.bet for player in self.game.players))

        self.actor._commitment += self.amount - self.actor.bet
        self.game.env._actor = next(self.actor)

    def verify(self) -> None:
        super().verify()

        if max(player._commitment for player in self.game.players) >= self.actor._total:
            raise ActionException('The stack of the acting player is covered')
        elif all(not player._is_relevant for player in self.game.players if player is not self.actor):
            raise ActionException('Betting/Raising is redundant')
        elif not self.stage.min_amount <= self.amount <= self.stage.max_amount:
            raise ActionException('The bet/raise amount is not allowed')


class ShowdownAction(PokerAction[PokerPlayer, ShowdownStage]):
    def __init__(self, game: PokerGame, actor: PokerPlayer, show: bool):
        super().__init__(game, actor)

        self.show = show

    def act(self) -> None:
        super().act()

        for player in self.game.players:
            if player is not self.actor and all(hole_card.status for hole_card in player._hole_cards) \
                    and player.hand > self.actor.hand and player._commitment >= self.actor._commitment:
                self.actor._muck()
                break
        else:
            self.show = True

        if self.show:
            for card in self.actor._hole_cards:
                card._status = True

        self.game.env._actor = next(self.actor)

        if self.game.env.actor is self.stage.opener:
            self.change_stage()

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, ShowdownStage):
            raise ActionException('Game not in showdown')
