from abc import ABC, abstractmethod

from pokertools import Card

from gameframe.game import ActionException
from gameframe.poker import CardCountException
from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.exceptions import InvalidPlayerException
from gameframe.poker.stages import BoardCardDealingStage, DealingStage, HoleCardDealingStage


class DealingAction(PokerAction[PokerNature], ABC):
    def __init__(self, game: PokerGame, actor: PokerNature, *cards: Card):
        super().__init__(game, actor)

        self.cards = list(cards)

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
        pass

    @property
    def next_actor(self) -> PokerNature:
        return self.game.nature


class HoleCardDealingAction(DealingAction):
    def __init__(self, game: PokerGame, actor: PokerNature, player: PokerPlayer, *cards: Card):
        super().__init__(game, actor, *cards)

        self.player = player

    def deal(self) -> None:
        self.player._hole_cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.player, PokerPlayer):
            raise TypeError('The player must be of type PokerPlayer')
        elif not isinstance(self.game._stage, HoleCardDealingStage):
            raise ActionException('Hole card dealing not allowed')
        elif self.player.mucked:
            raise InvalidPlayerException('Cannot deal to mucked player')
        elif len(self.player._hole_cards) >= self.game._stage.card_target:
            raise InvalidPlayerException('The player already has enough hole cards')
        elif len(self.cards) != self.game._stage.card_count:
            raise CardCountException('Invalid number of hole cards are dealt')


class BoardCardDealingAction(DealingAction):
    def deal(self) -> None:
        self.game._board_cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game._stage, BoardCardDealingStage):
            raise ActionException('Board card dealing not allowed')
        elif len(self.game.board_cards) >= self.game._stage.card_target:
            raise ActionException('The board already has enough cards')
        elif len(self.cards) != self.game._stage.card_count:
            raise CardCountException('Invalid number of board cards are dealt')
