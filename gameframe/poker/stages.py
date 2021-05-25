from abc import ABC

from auxiliary import after, rotated

from gameframe.poker.bases import Poker, Stage
from gameframe.poker.utilities import _collect


class DealingStage(Stage, ABC):
    """DealingStage is the class for dealing stages."""
    ...


class HoleDealingStage(DealingStage):
    """HoleDealingStage is the class for hole card dealing stages."""

    def __init__(self, deal_count: int, status: bool):
        self._deal_count = deal_count
        self._status = status

    def _done(self, game: Poker) -> bool:
        return super()._done(game) \
               or all(len(player.hole) == self._deal_target(game) for player in game.players if player.active)


class BoardDealingStage(DealingStage):
    """BoardDealingStage is the class for board card dealing stages."""

    def __init__(self, deal_count: int):
        self._deal_count = deal_count

    def _done(self, game: Poker) -> bool:
        return super()._done(game) or len(game.board) == self._deal_target(game)


class QueuedStage(Stage):
    """QueuedStage is the class for stages where players act in queued order."""

    _deal_count = 0

    def _done(self, game: Poker) -> bool:
        return super()._done(game) or (game.stage is not self and not game._queue)

    def _close(self, game: Poker) -> None:
        super()._close(game)

        game._queue.clear()


class BettingStage(Stage, ABC):
    """BettingStage is the class for betting stages."""

    def __init__(self, initial_max_delta: int):
        self.__initial_max_delta = initial_max_delta

    def _done(self, game: Poker) -> bool:
        return super()._done(game) or all(not player._relevant for player in game.players)

    def _open(self, game: Poker) -> None:
        super()._open(game)

        players = tuple(player for player in game.players if player._relevant)
        opener = after(players, max(players, key=lambda player: (player.bet, game.players.index(player))), True)

        game._actor = opener
        game._queue = list(rotated(players, players.index(opener)))[1:]
        game._max_delta = self.__initial_max_delta

        if any(player._bet for player in game.players):
            game._bet_raise_count = 1
        else:
            game._aggressor = opener
            game._bet_raise_count = 0

    def _close(self, game: Poker) -> None:
        super()._close(game)

        _collect(game)


class DiscardDrawStage(Stage):
    """DiscardDrawStage is the class for discard and draw stages."""

    def _open(self, game: Poker) -> None:
        super()._open(game)

        players = tuple(player for player in game.players if player.active)
        opener = next(player for player in game.players if player.active)

        game._actor = opener
        game._queue = list(rotated(players, players.index(opener)))[1:]


class ShowdownStage(Stage):
    def _open(self, game: Poker) -> None:
        super()._open(game)

        players = tuple(player for player in game.players if player.active)

        if game._aggressor is None or all(player.mucked or player._stack == 0 for player in game.players):
            opener = next(player for player in game.players if player.active)
        else:
            opener = game._aggressor

        game._actor = opener
        game._queue = list(rotated(players, players.index(opener)))[1:]
