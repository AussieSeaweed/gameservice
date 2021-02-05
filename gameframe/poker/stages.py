from abc import ABC, abstractmethod
from typing import Sequence, cast

from gameframe.poker.bases import PokerGame, PokerNature, PokerPlayer, Stage
from gameframe.utils import rotate


class DealingStage(Stage):
    def __init__(self, game: PokerGame, hole_card_statuses: Sequence[bool], board_card_count: int):
        super().__init__(game)

        self.hole_card_statuses = hole_card_statuses
        self.board_card_count = board_card_count

    @property
    def is_skippable(self) -> bool:
        return super().is_skippable \
               or (all(len(player._hole_cards) == self.target_hole_card_count for player in self.game.players if
                       not player.is_mucked)
                   and len(self.game.board_cards) == self.target_board_card_count)

    @property
    def opener(self) -> PokerNature:
        return self.game.nature


class BettingStage(Stage, ABC):
    def __init__(self, game: PokerGame, initial_max_delta: int):
        super().__init__(game)

        self.initial_max_delta = initial_max_delta

    @property
    def min_amount(self) -> int:
        return min(max(player.bet for player in self.game.players) + self.game._max_delta,
                   cast(PokerPlayer, self.game.actor).bet + cast(PokerPlayer, self.game.actor).stack)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    def is_skippable(self) -> bool:
        return super().is_skippable or all(not player._is_relevant for player in self.game.players) \
               or self.game.actor is self.game._aggressor

    @property
    def opener(self) -> PokerPlayer:
        index = (max(self.game.players, key=lambda player: (player.bet, player.index)).index + 1) \
                % len(self.game.players)

        return next(player for player in rotate(self.game.players, index) if player._is_relevant)

    def open(self) -> None:
        super().open()

        self.game._aggressor = self.opener
        self.game._max_delta = self.initial_max_delta

    def close(self) -> None:
        super().close()

        requirement = sorted(player._commitment for player in self.game.players)[-2]

        for player in self.game.players:
            player._commitment = min(player._commitment, requirement)

        self.game._requirement = requirement


class NLBettingStage(BettingStage):
    @property
    def max_amount(self) -> int:
        return cast(PokerPlayer, self.game.actor).bet + cast(PokerPlayer, self.game.actor).stack


class ShowdownStage(Stage):
    @property
    def is_skippable(self) -> bool:
        return super().is_skippable or all(player.is_mucked or player.is_shown for player in self.game.players)

    @property
    def opener(self) -> PokerPlayer:
        if all(player.is_mucked or player.stack == 0 for player in self.game.players):
            return next(player for player in self.game.players if not player.is_mucked)
        else:
            return self.game._aggressor
