from abc import ABC, abstractmethod
from typing import Optional, Sequence, cast

from gameframe.poker.bases import MidStage, OpenStage, PokerGame, PokerNature, PokerPlayer, Stage
from gameframe.poker.mixins import Closeable, Openable
from gameframe.utils import rotate


class SetupStage(Stage):
    def __next__(self) -> MidStage:
        return self.game.env._mid_stages[0]

    @property
    def is_skippable(self) -> bool:
        return True


class DistributionStage(OpenStage, Openable):
    def __next__(self) -> Stage:
        raise StopIteration

    @property
    def is_skippable(self) -> bool:
        return False

    @property
    def opener(self) -> PokerNature:
        return self.game.nature


class DealingStage(MidStage):
    def __init__(self, game: PokerGame, hole_card_statuses: Sequence[bool], board_card_count: int):
        super().__init__(game)

        self.hole_card_statuses = hole_card_statuses
        self.board_card_count = board_card_count

    @property
    def target_hole_card_count(self) -> int:
        count = len(self.hole_card_statuses)

        for stage in self.game.env._mid_stages[:self.index]:
            if isinstance(stage, DealingStage):
                count += len(stage.hole_card_statuses)

        return count

    @property
    def target_board_card_count(self) -> int:
        count = self.board_card_count

        for stage in self.game.env._mid_stages[:self.index]:
            if isinstance(stage, DealingStage):
                count += stage.board_card_count

        return count

    @property
    def is_skippable(self) -> bool:
        return super().is_skippable \
               or (all(len(player._hole_cards) == self.target_hole_card_count for player in self.game.players if
                       not player.is_mucked)
                   and len(self.game.env.board_cards) == self.target_board_card_count)

    @property
    def opener(self) -> PokerNature:
        return self.game.nature


class BettingStage(MidStage, Closeable, ABC):
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
    def is_skippable(self) -> bool:
        return super().is_skippable \
               or all(not player._is_relevant for player in self.game.players) \
               or self.game.env.actor is self.aggressor

    @property
    def opener(self) -> PokerPlayer:
        opener = min(self.game.players, key=lambda player: player.bet)

        return next(player for player in rotate(self.game.players, opener.index) if player._is_relevant)

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
        return cast(PokerPlayer, self.game.env.actor).bet + cast(PokerPlayer, self.game.env.actor).stack


class ShowdownStage(MidStage):
    @property
    def is_skippable(self) -> bool:
        return super().is_skippable or all(player.is_mucked or player.is_shown for player in self.game.players)

    @property
    def opener(self) -> PokerPlayer:
        if not all(player.is_mucked or player.stack == 0 for player in self.game.players):
            for stage in reversed(self.game.env._mid_stages):
                if isinstance(stage, BettingStage) and stage.aggressor is not None:
                    return stage.aggressor

        return next(player for player in self.game.players if not player.is_mucked)
