from abc import ABC, abstractmethod
from typing import Sequence, cast

from gameframe.poker.bases import PokerGame, PokerPlayer, Stage
from gameframe.utils import rotate


class OpenMixin(ABC):
    @abstractmethod
    def open(self) -> None:
        pass


class CloseMixin(ABC):
    @abstractmethod
    def close(self) -> None:
        pass


class SetupStage(Stage):
    pass


class DistributionStage(Stage, OpenMixin):
    def open(self) -> None:
        self.game.env._actor = self.game.nature


class MidStage(Stage, OpenMixin):
    @property
    def skip(self) -> bool:
        return sum(not player.is_mucked for player in self.game.players) == 1

    def open(self) -> None:
        assert not self.skip, 'DEBUG: Cannot open skipped round'


class DealingStage(MidStage):
    def __init__(self, game: PokerGame, hole_card_statuses: Sequence[bool], board_card_count: int):
        super().__init__(game)

        assert hole_card_statuses or board_card_count, 'DEBUG: Need to deal at least one hole or board card'

        self.hole_card_statuses = hole_card_statuses
        self.board_card_count = board_card_count

    @property
    def target_hole_card_count(self) -> int:
        count = len(self.hole_card_statuses)

        for stage in self.game.env._stages[:self.index]:
            if isinstance(stage, DealingStage):
                count += len(stage.hole_card_statuses)

        return count

    @property
    def target_board_card_count(self) -> int:
        count = self.board_card_count

        for stage in self.game.env._stages[:self.index]:
            if isinstance(stage, DealingStage):
                count += stage.board_card_count

        return count

    def open(self) -> None:
        super().open()

        self.game.env._actor = self.game.nature


class BettingStage(MidStage, CloseMixin, ABC):
    @property
    def min_amount(self) -> int:
        actor = cast(PokerPlayer, self.game.env.actor)

        return min(max(player.bet for player in self.game.players) + self.game.env._max_delta, actor.bet + actor.stack)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    def opener(self) -> PokerPlayer:
        opener = min(self.game.players, key=lambda player: player.bet)

        return next(player for player in rotate(self.game.players, opener.index) if player._is_relevant)

    @property
    def initial_max_delta(self) -> int:
        return max(self.game.env.blinds)

    @property
    def skip(self) -> bool:
        return super().skip or all(not player._is_relevant for player in self.game.players)

    def open(self) -> None:
        super().open()

        self.game.env._actor = self.opener
        self.game.env._max_delta = self.initial_max_delta
        self.game.env._aggressor = self.game.env._actor

    def close(self) -> None:
        self.game.env._requirement = max(player._commitment for player in self.game.players)


class NLBettingStage(BettingStage):
    @property
    def max_amount(self) -> int:
        player = cast(PokerPlayer, self.game.env.actor)

        return player.bet + player.stack


class ShowdownStage(MidStage):
    def open(self) -> None:
        super().open()

        if self.game.env._aggressor is None:
            self.game.env._aggressor = next(player for player in self.game.players if not player.is_mucked)

            assert self.game.env._aggressor is self.game.players[0], 'DEBUG: the first player cannot be mucked'

        self.game.env._actor = self.game.env._aggressor
