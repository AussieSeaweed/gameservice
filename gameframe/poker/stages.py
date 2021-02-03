from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union, cast

from gameframe.poker.bases import PokerGame, PokerNature, PokerPlayer, Stage
from gameframe.utils import rotate


class OpenMixin(ABC):
    @abstractmethod
    def open(self) -> None:
        pass


class CloseMixin(ABC):
    @abstractmethod
    def close(self) -> None:
        pass


class OpenStage(Stage, OpenMixin, ABC):
    @property
    @abstractmethod
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        pass

    def open(self) -> None:
        self.game.env._actor = self.opener


class MidStage(OpenStage, ABC):
    @property
    def skip(self) -> bool:
        return sum(not player.is_mucked for player in self.game.players) == 1

    def open(self) -> None:
        super().open()

        assert not self.skip, 'DEBUG: Cannot open skipped round'


class SetupStage(Stage):
    pass


class DistributionStage(OpenStage, OpenMixin):
    @property
    def opener(self) -> PokerNature:
        return self.game.nature


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

    @property
    def opener(self) -> PokerNature:
        return self.game.nature


class BettingStage(MidStage, CloseMixin, ABC):
    def __init__(self, game: PokerGame, initial_max_delta: int):
        super().__init__(game)

        self.aggressor: Optional[PokerPlayer] = None
        self.max_delta = initial_max_delta

    @property
    def min_amount(self) -> int:
        actor = cast(PokerPlayer, self.game.env.actor)

        return min(max(player.bet for player in self.game.players) + self.max_delta, actor.bet + actor.stack)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    def opener(self) -> PokerPlayer:
        opener = min(self.game.players, key=lambda player: player.bet)

        return next(player for player in rotate(self.game.players, opener.index) if player._is_relevant)

    @property
    def skip(self) -> bool:
        return super().skip or all(not player._is_relevant for player in self.game.players)

    def open(self) -> None:
        super().open()

        self.aggressor = self.opener

    def close(self) -> None:
        requirement = sorted(player._commitment for player in self.game.players)[-2]

        for player in self.game.players:
            player._commitment = min(player._commitment, requirement)

        self.game.env._requirement = requirement


class NLBettingStage(BettingStage):
    @property
    def max_amount(self) -> int:
        player = cast(PokerPlayer, self.game.env.actor)

        return player.bet + player.stack


class ShowdownStage(MidStage):
    @property
    def opener(self) -> PokerPlayer:
        if not all(player.is_mucked or player.stack == 0 for player in self.game.players):
            for stage in reversed(self.game.env._stages):
                if isinstance(stage, BettingStage) and stage.aggressor is not None:
                    return stage.aggressor

        return next(player for player in self.game.players if not player.is_mucked)
