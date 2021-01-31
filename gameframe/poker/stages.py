from abc import ABC, abstractmethod
from typing import Sequence, Union, cast

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


class SetupStage(Stage):
    pass


class DealingStage(Stage):
    def __init__(self, game: PokerGame, hole_card_statuses: Sequence[bool], board_card_count: int):
        super().__init__(game)

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
        self.game.env._actor = self.game.nature


class DistributionStage(Stage, OpenMixin):
    def open(self) -> None:
        self.game.env._actor = self.game.nature


class BettingStage(Stage, OpenMixin, CloseMixin, ABC):
    @property
    def min_amount(self) -> int:
        player = cast(PokerPlayer, self.game.env.actor)

        return min(max(p.bet for p in self.game.players) + self.game.env._max_delta, player.bet + player.stack)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        try:
            opener = min(self.game.players, key=lambda player: player.bet)

            return next(player for player in rotate(self.game.players, opener.index) if player._is_relevant)
        except StopIteration:
            return self.game.nature

    @property
    def initial_max_delta(self) -> int:
        return max(self.game.env.blinds)

    def open(self) -> None:
        self.game.env._actor = self.opener

        if isinstance(self.game.env._actor, PokerPlayer):
            self.game.env._max_delta = self.initial_max_delta
            self.game.env._aggressor = self.game.env._actor

    def close(self) -> None:
        self.game.env._requirement = max(player._commitment for player in self.game.players)


class NLBettingStage(BettingStage):
    @property
    def max_amount(self) -> int:
        player = cast(PokerPlayer, self.game.env.actor)

        return player.bet + player.stack


class ShowdownStage(Stage, OpenMixin):
    def open(self) -> None:
        self.game.env._actor = self.game.env._aggressor
