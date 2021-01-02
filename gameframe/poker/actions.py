from __future__ import annotations

from collections import defaultdict
from typing import Iterable, TYPE_CHECKING, final

from gameframe.poker.bases import PokerNatureAction, PokerPlayerAction
from gameframe.poker.exceptions import AmountOutOfBoundsException, FutileActionException
from gameframe.utils import override
from gameframe.utils import rotate

if TYPE_CHECKING:
    from gameframe.poker import Hand, PokerPlayer


@final
class SubmissiveAction(PokerPlayerAction):
    """SubmissiveAction is the class for folds."""

    @override
    def act(self) -> None:
        super().act()

        self.actor._muck()

        if sum(not player._mucked for player in self.game.players) == 1:
            self.game._actor = self.game.nature
        else:
            self.game._actor = next(self.actor)

    @override
    def __str__(self) -> str:
        return 'Fold'

    @override
    def _verify(self) -> None:
        super()._verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise FutileActionException()


@final
class PassiveAction(PokerPlayerAction):
    """PassiveAction is the class for checks and calls."""

    @override
    def act(self) -> None:
        super().act()

        amount: int = self.__amount

        self.actor._stack -= amount
        self.actor._bet += amount

        self.game._actor = next(self.actor)

    @override
    def __str__(self) -> str:
        return f'Call {self.__amount}' if self.__amount else 'Check'

    @property
    def __amount(self) -> int:
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)


@final
class AggressiveAction(PokerPlayerAction):
    """AggressiveAction is the class for bets and raises."""

    def __init__(self, actor: PokerPlayer, amount: int) -> None:
        super().__init__(actor)

        self.__amount: int = amount

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
    def __str__(self) -> str:
        return ('Raise ' if any(player.bet for player in self.game.players) else 'Bet ') + str(self.__amount)

    @override
    def _verify(self) -> None:
        super()._verify()

        if sum(player._relevant for player in self.game.players) <= 1:
            raise FutileActionException()
        if not (self.game._limit.min_amount <= self.__amount <= self.game._limit.max_amount):
            raise AmountOutOfBoundsException()


@final
class RoundAction(PokerNatureAction):
    """RoundAction is the class for round transitions and showdowns."""

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

    @override
    def __str__(self) -> str:
        return 'Next Street'

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
        players: list[PokerPlayer] = list(filter(lambda player: not player._mucked, self.game.players))
        base: int = 0

        for base_player in sorted(players, key=lambda player: (player._hand, player._commitment)):
            side_pot: int = self.__side_pot(base, base_player)

            recipients: list[PokerPlayer] = list(filter(lambda player: player._hand == base_player._hand, players))

            for recipient in recipients:
                recipient._bet += side_pot // len(recipients)
            else:
                recipients[0]._bet += side_pot % len(recipients)

            base = max(base, base_player._commitment)

        self.game.environment._pot = 0

        for player in players:
            player._stack += player.bet
            player._bet = 0

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot: int = 0

        for player in self.game.players:
            if base < (entitlement := min(player._commitment, base_player._commitment)):
                side_pot += entitlement - base

        return side_pot
