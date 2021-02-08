from abc import ABC, abstractmethod
from typing import cast

from gameframe.game import ActionException
from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.stages import DealingStage
from gameframe.poker.utils import CardLike, parse_card


class DealingAction(PokerAction[PokerNature], ABC):
    def __init__(self, game: PokerGame, actor: PokerNature, *cards: CardLike):
        super().__init__(game, actor)

        self.cards = list(map(parse_card, cards))

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
    def __init__(self, game: PokerGame, actor: PokerNature, player: PokerPlayer, *cards: CardLike):
        super().__init__(game, actor, *cards)

        self.player = player

    def deal(self) -> None:
        self.player._hole_cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        stage = cast(DealingStage, self.game._stage)

        if len(self.player._hole_cards) >= stage.hole_card_target:
            raise ActionException('The player already has enough hole cards')
        elif len(self.cards) != len(stage.hole_card_statuses):
            raise ActionException('Invalid number of hole cards are dealt')
        elif self.player.mucked:
            raise ActionException('Cannot deal to mucked player')


class BoardCardDealingAction(DealingAction):
    def deal(self) -> None:
        self.game._board_cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        stage = cast(DealingStage, self.game._stage)

        if len(self.game.board_cards) >= stage.board_card_target:
            raise ActionException('The board already has enough cards')
        elif len(self.cards) != stage.board_card_count:
            raise ActionException('Invalid number of board cards are dealt')
