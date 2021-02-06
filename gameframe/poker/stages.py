from abc import ABC, abstractmethod
from enum import Enum, unique
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
        self.flag = self.Flag.DEFAULT

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
               or (self.game.actor is self.game._aggressor and self.flag != self.Flag.IGNORE) \
               or self.flag == self.Flag.FINAL

    @property
    def opener(self) -> PokerPlayer:
        index = (max(self.game.players, key=lambda player: (player.bet, player.index)).index + 1) \
                % len(self.game.players)

        return next(player for player in rotate(self.game.players, index) if player._is_relevant)

    def open(self) -> None:
        super().open()

        if any(player.bet for player in self.game.players):
            self.flag = self.Flag.IGNORE
        else:
            self.game._aggressor = self.opener

        self.game._max_delta = self.initial_max_delta

    def close(self) -> None:
        super().close()

        self.game._trim()

    def update(self) -> None:
        if self.game.actor is self.game._aggressor:
            self.flag = self.Flag.FINAL

    @unique
    class Flag(Enum):
        DEFAULT = 0
        IGNORE = 1
        FINAL = 2


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
