from abc import ABC
from enum import Enum, auto
from typing import cast

from auxiliary.funcs import after, iindex
from math2.misc import bind

from gameframe.poker.bases import Limit, PokerGame, PokerNature, PokerPlayer, Stage


class DealingStage(Stage, ABC):
    """DealingStage is the class for dealing stages."""

    def __init__(self, card_count: int):
        self._card_count = card_count

    def _opener(self, game: PokerGame) -> PokerNature:
        return game.nature

    def _card_target(self, game: PokerGame) -> int:
        count = 0

        for stage in game._stages[:iindex(game._stages, self) + 1]:
            if isinstance(stage, type(self)):
                count += stage._card_count

        return count


class HoleDealingStage(DealingStage):
    """HoleDealingStage is the class for hole card dealing stages."""

    def __init__(self, card_count: int, status: bool):
        super().__init__(card_count)

        self._status = status

    def _skippable(self, game: PokerGame) -> bool:
        return super()._skippable(game) or all(
            len(player._hole_cards) == self._card_target(game) for player in game.players if not player.mucked
        )


class BoardDealingStage(DealingStage):
    """BoardDealingStage is the class for board card dealing stages."""

    def _skippable(self, game: PokerGame) -> bool:
        return super()._skippable(game) or len(game._board_cards) == self._card_target(game)


class BettingStage(Stage, ABC):
    """BettingStage is the class for betting stages."""

    def __init__(self, initial_max_delta: int):
        self._initial_max_delta = initial_max_delta

        self._behavior = self._Behavior.DEFAULT

    def _skippable(self, game: PokerGame) -> bool:
        return super()._skippable(game) or all(not player._relevant for player in game.players) \
               or (game._actor is game._aggressor and self._behavior != self._Behavior.IGNORE) \
               or self._behavior == self._Behavior.FINAL

    def _open(self, game: PokerGame) -> None:
        super()._open(game)

        if any(player._bet for player in game.players):
            self._behavior = self._Behavior.IGNORE
            game._bet_raise_count = 1
        else:
            game._aggressor = self._opener(game)
            game._bet_raise_count = 0

        game._max_delta = self._initial_max_delta

    def _close(self, game: PokerGame) -> None:
        game._reset()

    def _update(self, game: PokerGame) -> None:
        if game._actor is game._aggressor:
            self._behavior = self._Behavior.FINAL

    def _opener(self, game: PokerGame) -> PokerPlayer:
        relevant_players = tuple(player for player in game.players if player._relevant)
        sub_opener = max(relevant_players, key=lambda player: (player._bet, game.players.index(player)))

        return after(relevant_players, sub_opener, True)

    class _Behavior(Enum):
        DEFAULT = auto()
        IGNORE = auto()
        FINAL = auto()


class _ShowdownStage(Stage):
    def _skippable(self, game: PokerGame) -> bool:
        return super()._skippable(game) or all(player.mucked or player.shown for player in game.players)

    def _opener(self, game: PokerGame) -> PokerPlayer:
        if all(player.mucked or player._stack == 0 for player in game.players):
            return next(player for player in game.players if not player.mucked)
        else:
            return game._aggressor


class FixedLimit(Limit):
    """FixedLimit is the class for fixed-limits."""

    _max_bet_raise_count = 4

    def _max_amount(self, game: PokerGame) -> int:
        return self._min_amount(game)


class PotLimit(Limit):
    """PotLimit is the class for pot-limits."""

    _max_bet_raise_count = None

    def _max_amount(self, game: PokerGame) -> int:
        bets = tuple(player._bet for player in game.players)
        actor = cast(PokerPlayer, game._actor)

        return bind(max(bets) + game._pot + sum(bets) + max(bets) - actor._bet, game._max_delta, actor._total)


class NoLimit(Limit):
    """NoLimit is the class for no-limits."""

    _max_bet_raise_count = None

    def _max_amount(self, game: PokerGame) -> int:
        return cast(PokerPlayer, game._actor)._total
