from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import cast

from math2.utils import after, bind
from pokertools import Card, HoleCard

from gameframe.exceptions import ActionException
from gameframe.game import _A
from gameframe.poker.bases import Poker, PokerNature, PokerPlayer
from gameframe.poker.exceptions import BetRaiseAmountException, CardCountException, PlayerException
from gameframe.poker.parameters import (BettingStage, BoardDealingStage, DealingStage, DiscardDrawStage,
                                        HoleDealingStage,
                                        _ShowdownStage)
from gameframe.sequential import _SequentialAction


class PokerAction(_SequentialAction[Poker, _A], ABC):
    def act(self) -> None:
        super().act()

        if self.game._stage._skippable(self.game):
            self.game._stage._close(self.game)

            try:
                self.game._stage = after(self.game._stages, self.game._stage)

                while self.game._stage._skippable(self.game):
                    self.game._stage = after(self.game._stages, self.game._stage)
                else:
                    self.game._stage._open(self.game)
            except ValueError:
                self.game._reset()
                self.distribute()
                self.game._actor = None
        else:
            self.game._stage._update(self.game)

    def distribute(self) -> None:
        players = [player for player in self.game.players if not player.mucked]

        if len(players) > 1:
            players.sort(key=lambda player: (player.hand, -player._put), reverse=True)

        base = 0

        for base_player in players:
            if base < base_player._put:
                side_pot = self.side_pot(base, base_player._put)
                winners = tuple(
                    player for player in players if player is base_player or player.hand == base_player.hand)

                for winner in winners:
                    winner._bet += side_pot // len(winners)
                else:
                    winners[0]._bet += side_pot % len(winners)

                base = max(base, base_player._put)

        for player in self.game.players:
            if player._put > base:
                player._bet += player._put - base

            player._stack += player._bet
            player._bet = 0

        self.game._pot = 0

    def side_pot(self, lo: int, hi: int) -> int:
        side_pot = 0

        for player in self.game.players:
            side_pot += bind(player._put, lo, hi) - lo

        return side_pot


class DealingAction(PokerAction[PokerNature], ABC):
    def __init__(self, game: Poker, actor: PokerNature, cards: Iterable[Card]):
        super().__init__(game, actor)

        self.cards = tuple(cards)

    @property
    def next_actor(self) -> PokerNature:
        return self.game.nature

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, DealingStage):
            raise ActionException('Dealing not allowed')
        elif any(card not in self.game._deck for card in self.cards):
            raise ActionException('Card not in deck')
        elif len(self.cards) != len(set(self.cards)):
            raise ActionException('Duplicates in cards')
        elif len(self.cards) != self.game._stage._card_count:
            raise CardCountException('Invalid number of hole cards are dealt')

    def apply(self) -> None:
        self.game._deck.draw(self.cards)
        self.deal()

    @abstractmethod
    def deal(self) -> None:
        pass


class HoleDealingAction(DealingAction):
    def __init__(self, game: Poker, actor: PokerNature, player: PokerPlayer, cards: Iterable[Card]):
        super().__init__(game, actor, cards)

        self.player = player

    def verify(self) -> None:
        if not isinstance(self.player, PokerPlayer):
            raise TypeError('The player must be of type PokerPlayer')
        elif not isinstance(self.game._stage, HoleDealingStage):
            raise ActionException('Hole card dealing not allowed')
        elif self.player.mucked:
            raise PlayerException('Cannot deal to mucked player')
        elif len(self.player._hole) >= self.game._stage._card_target(self.game):
            raise PlayerException('The player already has enough hole cards')

        super().verify()

    def deal(self) -> None:
        status = cast(HoleDealingStage, self.game._stage)._status

        self.player._hole.extend(HoleCard(card, status) for card in self.cards)


class BoardDealingAction(DealingAction):
    def verify(self) -> None:
        if not isinstance(self.game._stage, BoardDealingStage):
            raise ActionException('Board card dealing not allowed')
        elif len(self.game._board) >= self.game._stage._card_target(self.game):
            raise ActionException('The board already has enough cards')

        super().verify()

    def deal(self) -> None:
        self.game._board.extend(self.cards)


class BettingAction(PokerAction[PokerPlayer], ABC):
    @property
    def next_actor(self) -> PokerPlayer:
        actor = after(self.game.players, self.actor, True)

        while not actor._relevant and actor is not self.game._aggressor:
            actor = after(self.game.players, actor, True)

        return actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, BettingStage):
            raise ActionException('Not a betting round')


class FoldAction(BettingAction):
    def verify(self) -> None:
        super().verify()

        if self.actor._bet >= max(player._bet for player in self.game.players):
            raise ActionException('Folding is redundant')

    def apply(self) -> None:
        self.actor._status = self.actor._Status.MUCKED


class CheckCallAction(BettingAction):
    @property
    def amount(self) -> int:
        return min(self.actor._stack, max(player._bet for player in self.game.players) - self.actor._bet)

    def apply(self) -> None:
        amount = self.amount

        self.actor._stack -= amount
        self.actor._bet += amount


class BetRaiseAction(BettingAction):
    def __init__(self, game: Poker, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.amount = amount

    def verify(self) -> None:
        super().verify()

        if max(player._bet for player in self.game.players) >= self.actor._total:
            raise ActionException('The stack of the acting player is covered')
        elif all(not player._relevant for player in self.game.players if player is not self.actor):
            raise ActionException('Betting/Raising is redundant')
        elif self.game._bet_raise_count == self.game._limit._max_count:
            raise ActionException('Too many number of bets/raises')
        elif not self.game._limit._min_amount(self.game) <= self.amount <= self.game._limit._max_amount(self.game):
            raise BetRaiseAmountException('The bet/raise amount is not allowed')

    def apply(self) -> None:
        stage = cast(BettingStage, self.game._stage)
        stage._behavior = stage._Behavior.DEFAULT

        self.game._aggressor = self.actor
        self.game._max_delta = max(self.game._max_delta, self.amount - max(player._bet for player in self.game.players))
        self.game._bet_raise_count += 1

        self.actor._stack -= self.amount - self.actor._bet
        self.actor._bet = self.amount


class DiscardDrawAction(PokerAction[PokerPlayer]):
    def __init__(self, game: Poker, actor: PokerPlayer, discards: Iterable[Card], draws: Iterable[Card]):
        super().__init__(game, actor)

        self.discards = tuple(discards)
        self.draws = tuple(draws)

    @property
    def next_actor(self) -> PokerPlayer:
        actor = after(self.game.players, self.actor, True)

        while actor.mucked:
            actor = after(self.game.players, actor, True)

        return actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, DiscardDrawStage):
            raise ActionException('Not a draw round')
        elif any(from_ not in self.actor._hole for from_ in self.discards):
            raise ActionException('The hole card does not belong to the actor.')
        elif any(card not in self.game._deck for card in self.draws):
            raise ActionException('Card not in deck')
        elif len(self.discards) + len(self.draws) != len(set(self.discards) | set(self.draws)):
            raise ActionException('Duplicates in cards')
        elif len(self.discards) != len(self.draws):
            raise CardCountException('The from cards must be of same length as to cards.')

    def apply(self) -> None:
        self.game._deck.draw(self.draws)

        for i, card in enumerate(self.actor._hole):
            if card in self.discards:
                self.actor._hole[i] = HoleCard(self.draws[self.discards.index(card)], card.status)


class ShowdownAction(PokerAction[PokerPlayer]):
    def __init__(self, game: Poker, actor: PokerPlayer, force: bool) -> None:
        super().__init__(game, actor)

        self.force = force

    @property
    def next_actor(self) -> PokerPlayer:
        actor = after(self.game.players, self.actor, True)

        while actor.mucked:
            actor = after(self.game.players, actor, True)

        return actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, _ShowdownStage):
            raise ActionException('Game not in showdown')

    def apply(self) -> None:
        if self.force or all(not (player.hand > self.actor.hand and player._put >= self.actor._put)
                             for player in self.game.players if player.shown):
            self.actor._status = self.actor._Status.SHOWN
        else:
            self.actor._status = self.actor._Status.MUCKED
