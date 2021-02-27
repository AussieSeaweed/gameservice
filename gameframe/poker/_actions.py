from abc import ABC, abstractmethod
from collections import Iterable

from pokertools import Card

from gameframe.exceptions import ActionException
from gameframe.poker._bases import PokerAction, PokerGame, PokerNature, PokerPlayer, S
from gameframe.poker._exceptions import BetRaiseAmountException, CardCountException, InvalidPlayerException
from gameframe.poker._stages import (BettingFlag, BettingStage, BoardCardDealingStage, DealingStage,
                                     HoleCardDealingStage, ShowdownStage)


class DealingAction(PokerAction[PokerNature, S], ABC):
    def __init__(self, game: PokerGame, actor: PokerNature, cards: Iterable[Card]):
        super().__init__(game, actor)

        self.cards = tuple(cards)

    @property
    def next_actor(self) -> PokerNature:
        return self.game.nature

    def apply(self) -> None:
        self.deal()
        self.game._deck.remove(self.cards)

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, DealingStage):
            raise ActionException('Dealing not allowed')
        elif any(card not in self.game._deck for card in self.cards):
            raise ActionException('Card not in deck')
        elif len(self.cards) != len(set(self.cards)):
            raise ActionException('Duplicates in cards')

    @abstractmethod
    def deal(self) -> None:
        ...


class HoleCardDealingAction(DealingAction[HoleCardDealingStage]):
    def __init__(self, game: PokerGame, actor: PokerNature, player: PokerPlayer, cards: Iterable[Card]):
        super().__init__(game, actor, cards)

        self.player = player

    def deal(self) -> None:
        self.player._cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.player, PokerPlayer):
            raise TypeError('The player must be of type PokerPlayer')
        elif not isinstance(self.game._stage, HoleCardDealingStage):
            raise ActionException('Hole card dealing not allowed')
        elif self.player.mucked:
            raise InvalidPlayerException('Cannot deal to mucked player')
        elif len(self.player._cards) >= self.stage.card_target:
            raise InvalidPlayerException('The player already has enough hole cards')
        elif len(self.cards) != self.stage.card_count:
            raise CardCountException('Invalid number of hole cards are dealt')


class BoardCardDealingAction(DealingAction[BoardCardDealingStage]):
    def deal(self) -> None:
        self.game._board_cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, BoardCardDealingStage):
            raise ActionException('Board card dealing not allowed')
        elif len(self.game.board_cards) >= self.stage.card_target:
            raise ActionException('The board already has enough cards')
        elif len(self.cards) != self.stage.card_count:
            raise CardCountException('Invalid number of board cards are dealt')


class BettingAction(PokerAction[PokerPlayer, BettingStage], ABC):
    @property
    def next_actor(self) -> PokerPlayer:
        actor = next(self.actor)

        while not actor._relevant and actor is not self.game._aggressor:
            actor = next(actor)

        return actor

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, BettingStage):
            raise ActionException('Not a betting round')


class FoldAction(BettingAction):
    def apply(self) -> None:
        self.actor._status = self.actor._HoleCardStatus.MUCKED

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
        self.stage.flag = BettingFlag.DEFAULT

        self.game._aggressor = self.actor
        self.game._max_delta = max(self.game._max_delta, self.amount - max(player.bet for player in self.game.players))

        self.actor._commitment += self.amount - self.actor.bet

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.amount, int):
            raise TypeError('The amount must be of type int')
        elif max(player._commitment for player in self.game.players) >= self.actor.starting_stack:
            raise ActionException('The stack of the acting player is covered')
        elif all(not player._relevant for player in self.game.players if player is not self.actor):
            raise ActionException('Betting/Raising is redundant')
        elif not self.stage.min_amount <= self.amount <= self.stage.max_amount:
            raise BetRaiseAmountException('The bet/raise amount is not allowed')


class ShowdownAction(PokerAction[PokerPlayer, ShowdownStage]):
    def __init__(self, game: PokerGame, actor: PokerPlayer, force: bool) -> None:
        super().__init__(game, actor)

        self.force = force

    @property
    def next_actor(self) -> PokerPlayer:
        actor = next(self.actor)

        while actor.mucked:
            actor = next(actor)

        return actor

    def apply(self) -> None:
        if self.force or all(not (player.hand > self.actor.hand and player._commitment >= self.actor._commitment)
                             for player in self.game.players if player.shown):
            self.actor._status = self.actor._HoleCardStatus.SHOWN
        else:
            self.actor._status = self.actor._HoleCardStatus.MUCKED

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.force, bool):
            raise TypeError('The force argument must be of type bool')
        elif not isinstance(self.game._stage, ShowdownStage):
            raise ActionException('Game not in showdown')
