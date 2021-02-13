from abc import ABC, abstractmethod
from enum import Enum, unique
from functools import cached_property
from typing import cast

from gameframe.poker.bases import PokerGame, PokerNature, PokerPlayer, Stage
from gameframe.utils import rotate


class DealingStage(Stage, ABC):
    def __init__(self, game: PokerGame, card_count: int):
        super().__init__(game)

        self.card_count = card_count

    @property
    def opener(self) -> PokerNature:
        return self.game.nature

    @cached_property
    @abstractmethod
    def card_target(self) -> int:
        pass


class HoleCardDealingStage(DealingStage):
    def __init__(self, game: PokerGame, card_count: int, card_status: bool):
        super().__init__(game, card_count)

        self.card_status = card_status

    @property
    def skippable(self) -> bool:
        return super().skippable or all(len(player._hole_cards) == self.card_target
                                        for player in self.game.players if not player.mucked)

    @cached_property
    def card_target(self) -> int:
        count = 0

        for stage in self.game._stages[:self.index + 1]:
            if isinstance(stage, HoleCardDealingStage):
                count += stage.card_count

        return count


class BoardCardDealingStage(DealingStage):
    @property
    def skippable(self) -> bool:
        return super().skippable or len(self.game.board_cards) == self.card_target

    @cached_property
    def card_target(self) -> int:
        count = 0

        for stage in self.game._stages[:self.index + 1]:
            if isinstance(stage, BoardCardDealingStage):
                count += stage.card_count

        return count


class BettingStage(Stage, ABC):
    def __init__(self, game: PokerGame, initial_max_delta: int):
        super().__init__(game)

        self.initial_max_delta = initial_max_delta
        self.flag = BettingFlag.DEFAULT

    @property
    def min_amount(self) -> int:
        player = cast(PokerPlayer, self.game.actor)

        return min(max(player.bet for player in self.game.players) + self.game._max_delta,
                   player.bet + player.stack)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    def skippable(self) -> bool:
        return super().skippable or all(not player._relevant for player in self.game.players) \
               or (self.game.actor is self.game._aggressor and self.flag != BettingFlag.IGNORE) \
               or self.flag == BettingFlag.FINAL

    @property
    def opener(self) -> PokerPlayer:
        index: int = next(max(self.game.players, key=lambda player: (player.bet, player.index))).index  # type: ignore

        return next(player for player in rotate(self.game.players, index) if player._relevant)

    def open(self) -> None:
        super().open()

        if any(player.bet for player in self.game.players):
            self.flag = BettingFlag.IGNORE
        else:
            self.game._aggressor = self.opener

        self.game._max_delta = self.initial_max_delta

    def close(self) -> None:
        super().close()

        self.game._trim()

    def update(self) -> None:
        if self.game.actor is self.game._aggressor:
            self.flag = BettingFlag.FINAL


class NLBettingStage(BettingStage):
    @property
    def max_amount(self) -> int:
        player = cast(PokerPlayer, self.game.actor)

        return player.bet + player.stack


class ShowdownStage(Stage):
    @property
    def skippable(self) -> bool:
        return super().skippable or all(player.mucked or player.shown for player in self.game.players)

    @property
    def opener(self) -> PokerPlayer:
        if all(player.mucked or player.stack == 0 for player in self.game.players):
            return next(player for player in self.game.players if not player.mucked)
        else:
            return self.game._aggressor


@unique
class BettingFlag(Enum):
    DEFAULT = 0
    IGNORE = 1
    FINAL = 2
