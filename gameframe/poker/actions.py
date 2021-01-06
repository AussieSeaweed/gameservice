from __future__ import annotations

from abc import ABC
from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, final

from gameframe.poker.bases import PokerNatureAction, PokerPlayerAction
from gameframe.poker.exceptions import AmountOutOfBoundsException, FutileActionException, InvalidRoundException, UnavailableActionException
from gameframe.utils import override
from gameframe.utils import rotate

if TYPE_CHECKING:
    from gameframe.poker import Hand, PokerPlayer

__all__: Sequence[str] = ['BettingRoundAction', 'FoldAction', 'CheckCallAction', 'BetRaiseAction', 'ProgressiveAction']


class BettingRoundAction(PokerPlayerAction, ABC):
    """BettingRoundAction is the abstract base class for all player actions in a betting round."""

    def _verify(self) -> None:
        from gameframe.poker import BettingRound

        if not isinstance(self.game._round, BettingRound):
            raise InvalidRoundException()


@final
class FoldAction(PokerPlayerAction):
    """FoldAction is the class for folds."""

    @override
    def __str__(self) -> str:
        return 'Fold'

    @override
    def act(self) -> None:
        super().act()

        self.actor._muck()

        if sum(not player._mucked for player in self.game.players) == 1:
            self.game._actor = self.game.nature
        else:
            self.game._actor = next(self.actor)

    @override
    def _verify(self) -> None:
        super()._verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise FutileActionException()


@final
class CheckCallAction(PokerPlayerAction):
    """CheckCallAction is the class for checks and calls."""

    @override
    def __str__(self) -> str:
        return f'Call {self.__amount}' if self.__amount else 'Check'

    @override
    def act(self) -> None:
        super().act()

        amount: int = self.__amount

        self.actor._stack -= amount
        self.actor._bet += amount

        self.game._actor = next(self.actor)

    @property
    def __amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)


@final
class BetRaiseAction(PokerPlayerAction):
    """BetRaiseAction is the class for bets and raises."""

    def __init__(self, actor: PokerPlayer, amount: int) -> None:
        super().__init__(actor)

        self.__amount: int = amount

    @override
    def __str__(self) -> str:
        return ('Raise ' if any(player.bet for player in self.game.players) else 'Bet ') + str(self.__amount)

    @override
    def act(self) -> None:
        super().act()

        self.game.environment._max_delta = max(self.game.environment._max_delta,
                                               self.__amount - max(player.bet for player in self.game.players))

        self.actor._stack -= self.__amount - self.actor.bet
        self.actor._bet = self.__amount

        self.game.environment._aggressor = self.actor
        self.game._actor = next(self.actor)

    @override
    def _verify(self) -> None:
        super()._verify()

        if sum(player._relevant for player in self.game.players) <= 1:
            raise FutileActionException()
        elif max(player.bet for player in self.game.players) < self.actor.stack:
            raise UnavailableActionException()
        elif not (self.game._limit.min_amount <= self.__amount <= self.game._limit.max_amount):
            raise AmountOutOfBoundsException()


@final
class ProgressiveAction(PokerNatureAction):
    """ProgressiveAction is the class for round transitions and showdowns."""

    @override
    def __str__(self) -> str:
        return 'Progress'

    @override
    def act(self) -> None:
        super().act()

        if self.game._round is not None:
            self.game._round._close()

        if sum(not player._mucked for player in self.game.players) == 1:
            self.game._rounds.clear()
        else:
            self.game._rounds.pop(0)

        if self.game._round is None:
            if sum(not player._mucked for player in self.game.players) > 1:
                self.__show()

            self.__distribute()

            self.game._actor = None
        else:
            self.game._round._open()

            self.game._actor = self.game._round._opener

    def __show(self) -> None:
        players: Iterable[PokerPlayer] = filter(
            lambda player: not player._mucked,
            self.game.players if self.game.environment._aggressor is None else rotate(
                self.game.players, self.game.environment._aggressor.index),
        )

        commitments: defaultdict[Hand, int] = defaultdict(lambda: 0)

        for player in players:
            for hand, commitment in commitments.items():
                if hand < player._hand and commitment >= player._commitment:
                    player._muck()
                    break
            else:
                commitments[player._hand] = max(commitments[player._hand], player._commitment)

                for card in player.hole_cards:
                    card._status = True

    def __distribute(self) -> None:
        base: int = 0

        players: Sequence[PokerPlayer] = list(filter(lambda player: not player._mucked, self.game.players))

        for base_player in sorted(players, key=lambda player: (player._hand, player._commitment)):
            side_pot: int = self.__side_pot(base, base_player)

            recipients: Sequence[PokerPlayer] = list(filter(lambda player: player._hand == base_player._hand, players))

            for recipient in recipients:
                recipient._bet += side_pot // len(recipients)
            else:
                recipients[0]._bet += side_pot % len(recipients)

            base: int = max(base, base_player._commitment)

        for player in self.game.players:
            if base < player._commitment:
                player._bet += player._commitment - base

            player._stack += player.bet
            player._bet = 0

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot: int = 0

        for player in self.game.players:
            if base < (entitlement := min(player._commitment, base_player._commitment)):
                side_pot += entitlement - base

        return side_pot
