from abc import ABC, abstractmethod
from itertools import zip_longest
from typing import cast

from gameframe.game import ActionException
from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.stages import DealingStage, DistributionStage, SetupStage
from gameframe.poker.utils import HoleCard
from gameframe.poker.utils.cards import CardLike, parse_card


class SetupAction(PokerAction[PokerNature]):
    def act(self) -> None:
        blinds = list(reversed(self.game.env.blinds)) if len(self.game.players) == 2 else self.game.env.blinds

        for player, blind in zip_longest(self.game.players, blinds, fillvalue=0):
            player._commitment = min(self.game.env.ante + blind, player._total)

        self.game.env._requirement = self.game.env.ante

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, SetupStage):
            raise ActionException('Already set up')

    @property
    def next_actor(self) -> PokerNature:
        return self.game.nature


class DealingAction(PokerAction[PokerNature], ABC):
    def __init__(self, game: PokerGame, actor: PokerNature, *cards: CardLike):
        super().__init__(game, actor)

        self.cards = list(map(parse_card, cards))

    def act(self) -> None:
        self.deal()
        self.game.env._deck.remove(self.cards)

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, DealingStage):
            raise ActionException('Dealing not allowed')
        elif any(card not in self.game.env._deck for card in self.cards):
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
        stage = cast(DealingStage, self.game.env._stage)

        self.player._hole_cards.extend(
            HoleCard(card, status) for card, status in zip(self.cards, stage.hole_card_statuses))

    def verify(self) -> None:
        super().verify()

        stage = cast(DealingStage, self.game.env._stage)

        if len(self.player._hole_cards) >= stage.target_hole_card_count:
            raise ActionException('The player already has enough hole cards')
        elif len(self.cards) != len(stage.hole_card_statuses):
            raise ActionException('Invalid number of hole cards are dealt')
        elif self.player.is_mucked:
            raise ActionException('Cannot deal to mucked player')


class BoardCardDealingAction(DealingAction):
    def deal(self) -> None:
        self.game.env._board_cards.extend(self.cards)

    def verify(self) -> None:
        super().verify()

        stage = cast(DealingStage, self.game.env._stage)

        if len(self.game.env.board_cards) >= stage.target_board_card_count:
            raise ActionException('The board already has enough cards')
        elif len(self.cards) != stage.board_card_count:
            raise ActionException('Invalid number of board cards are dealt')


class DistributionAction(PokerAction[PokerNature]):
    @property
    def next_actor(self) -> None:
        return None

    def act(self) -> None:
        players = list(filter(lambda player: not player.is_mucked, self.game.players))

        if len(players) > 1:
            players.sort(key=lambda player: (player.hand, -player._commitment), reverse=True)

        base = 0

        for base_player in players:
            side_pot = self.__side_pot(base, base_player)

            recipients = list(filter(lambda player: player is base_player or player.hand == base_player.hand, players))

            for recipient in recipients:
                recipient._total += side_pot // len(recipients)
            else:
                recipients[0]._total += side_pot % len(recipients)

            base = max(base, base_player._commitment)

        self.game.env._actor = None

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot = 0

        for player in self.game.players:
            entitlement = min(player._commitment, base_player._commitment)

            if base < entitlement:
                side_pot += entitlement - base

        return side_pot

    def verify(self) -> None:
        super().verify()

        if not isinstance(self.game.env._stage, DistributionStage):
            raise ActionException('Cannot distribute yet')
