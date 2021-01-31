from abc import ABC
from typing import cast

from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.rounds import BettingRound, DistributionRound, ShowdownRound
from gameframe.utils import rotate


class BettingAction(PokerAction[PokerPlayer], ABC):
    """BettingRoundAction is the abstract base class for all player actions in a betting round."""

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self.game.env.actor, PokerPlayer) \
               and isinstance(self.game.env._round, BettingRound)


class FoldAction(BettingAction):
    """FoldAction is the class for folds."""

    def __str__(self) -> str:
        return 'Fold'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self.actor.bet < max(player.bet for player in self.game.players)

    def act(self) -> None:
        super().act()

        self.actor._muck()

        if sum(not player.is_mucked for player in self.game.players) == 1:
            self.game.env._actor = self.game.nature
            self.game.env._round = DistributionRound(self.game)
        else:
            self.game.env._actor = next(self.actor)

            if isinstance(self.game.env.actor, PokerNature):
                self._change_round()


class CheckCallAction(BettingAction):
    """CheckCallAction is the class for checks and calls."""

    def __str__(self) -> str:
        return f'Call {self.__amount}' if self.__amount else 'Check'

    @property
    def __amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self) -> None:
        super().act()

        self.actor._commitment += self.__amount
        self.game.env._actor = next(self.actor)

        if isinstance(self.game.env.actor, PokerNature):
            self._change_round()


class BetRaiseAction(BettingAction):
    """BetRaiseAction is the class for bets and raises."""

    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.__amount = amount

    def __str__(self) -> str:
        return ('Raise ' if any(player.bet for player in self.game.players) else 'Bet ') + str(self.__amount)

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable \
               and max(player._commitment for player in self.game.players) < self.actor._total \
               and any(player._is_relevant for player in self.game.players if player is not self.actor) \
               and cast(BettingRound, self.game.env._round).min_amount <= self.__amount \
               <= cast(BettingRound, self.game.env._round).max_amount

    def act(self) -> None:
        super().act()

        self.game.env._aggressor = self.actor
        self.game.env._max_delta = max(self.game.env._max_delta,
                                       self.__amount - max(player.bet for player in self.game.players))
        self.actor._commitment += self.__amount - self.actor.bet
        self.game.env._actor = next(self.actor)


class ShowdownAction(PokerAction[PokerPlayer]):
    """ShowdownAction is the class for showdowns."""

    def __init__(self, game: PokerGame, actor: PokerPlayer, show: bool):
        super().__init__(game, actor)

        self.__show = show

    def __str__(self) -> str:
        return 'Show Cards' if self.__show else 'Showdown'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self.actor, PokerPlayer) \
               and isinstance(self.game.env._round, ShowdownRound)

    def act(self) -> None:
        players = list(filter(lambda p: not p.is_mucked, rotate(self.game.players, self.game.players.index(
            self.game.env._aggressor))))

        for player in players[:players.index(self.actor)]:
            if player.hand < self.actor.hand and player._commitment >= self.actor._commitment:
                player._muck()
                break
        else:
            self.__show = True

        if self.__show:
            for card in self.actor.hole_cards:
                card._status = True

        if players[-1] is self.actor:
            self._change_round()
        else:
            self.game.env._actor = players[players.index(self.actor) + 1]
