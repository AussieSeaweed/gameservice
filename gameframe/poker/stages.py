from abc import ABC, abstractmethod
from itertools import combinations
from typing import MutableSequence, Sequence

from gameframe.poker import Card
from gameframe.poker.actions import (BetRaiseAction, BettingAction, BoardCardDealingAction, CheckCallAction,
                                     DealingAction, DistributingAction, FoldAction, HoleCardDealingAction,
                                     ShowdownAction)
from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer, Stage
from gameframe.poker.utils import HoleCard


class BettingStage(Stage, ABC):
    """BettingStage is the class for betting rounds."""

    def __init__(self, game: PokerGame, board_card_count: int, hole_card_statuses: Sequence[bool]):
        super().__init__(game)

        self._game = game
        self._board_card_count = board_card_count
        self._hole_card_statuses = hole_card_statuses

    @property
    def nature_actions(self) -> Sequence[DealingAction[Card]]:
        actions: MutableSequence[DealingAction[Card]] = []

        if len(self._game.env.board_cards) < self.target_board_card_count:
            for cards in combinations(self.game.env._deck, self._board_card_count):
                actions.append(BoardCardDealingAction(self._game, self._game.nature, cards))
        else:
            for cards in combinations(self.game.env._deck, len(self._hole_card_statuses)):
                hole_cards = [HoleCard(card, status) for card, status in zip(cards, self._hole_card_statuses)]

                actions.append(HoleCardDealingAction(self._game, self._game.nature, hole_cards))

        return actions

    @property
    def player_actions(self) -> Sequence[BettingAction]:
        actions = [FoldAction(self._game, self.player), CheckCallAction(self._game, self.player)]

        for amount in range(self.min_amount, self.max_amount + 1):
            actions.append(BetRaiseAction(self._game, self.player, amount))

        return list(filter(lambda action: action.is_applicable, actions))

    @property
    def target_board_card_count(self) -> int:
        count = 0

        for stage in self._game.env._stages[:self._game.env._stages.index(self)]:
            if isinstance(stage, BettingStage):
                count += stage._board_card_count

        return count

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    @abstractmethod
    def min_amount(self) -> int:
        pass


class NLBettingStage(BettingStage):
    """NLBettingStage is the class for no-limit betting rounds."""

    @property
    def max_amount(self) -> int:
        return self.player.bet + self.player.stack

    @property
    def min_amount(self) -> int:
        return min(max(player.bet for player in self._game.players) + self._game.env._max_delta,
                   self.player.bet + self.player.stack)


class ShowdownStage(Stage):
    """ShowdownStage is the class for showdowns."""

    @property
    def nature_actions(self) -> Sequence[PokerAction[PokerNature]]:
        return [DistributingAction(self.game, self.game.nature)]

    @property
    def player_actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        return [ShowdownAction(self.game, self.player, False), ShowdownAction(self.game, self.player, True)]
