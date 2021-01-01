from __future__ import annotations

from collections import defaultdict
from typing import Iterable, TYPE_CHECKING

from gameframe.poker.bases import PokerNatureAction, PokerPlayerAction
from gameframe.utils import rotate

if TYPE_CHECKING:
    from gameframe.poker import PokerPlayer, Hand


class SubmissiveAction(PokerPlayerAction):
    """SubmissiveAction is the class for folds."""

    def act(self) -> None:
        super().act()

        self.actor._muck()

        if sum(not player.mucked for player in self.game.players) == 1:
            self.game._actor = self.game.nature
        else:
            self.game._actor = next(self.actor)

    def __str__(self) -> str:
        return 'Fold'

    def _verify(self) -> None:
        super()._verify()

        if self.actor.bet >= max(player.bet for player in self.game.players):
            raise ValueError('Player cannot fold if enough amount is already bet')


class PassiveAction(PokerPlayerAction):
    """PassiveAction is the class for checks and calls."""

    @property
    def amount(self) -> int:
        """
        :return: the call/check amount of the passive action
        """
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self) -> None:
        super().act()

        amount: int = self.amount

        self.actor.stack -= amount
        self.actor.bet += amount

        self.game._actor = next(self.actor)

    def __str__(self) -> str:
        return f'Call {self.amount}' if self.amount else 'Check'


class AggressiveAction(PokerPlayerAction):
    """AggressiveAction is the class for bets and raises."""

    def __init__(self, actor: PokerPlayer, amount: int) -> None:
        super().__init__(actor)

        self.__amount: int = amount

    def act(self) -> None:
        super().act()

        self.game.environment._max_delta = max(self.game.environment._max_delta,
                                               self.__amount - max(player.bet for player in self.game.players))

        self.actor._stack -= self.__amount - self.actor.bet
        self.actor._bet = self.__amount

        self.game.environment._aggressor = self.actor
        self.game._actor = next(self.actor)

    def __str__(self) -> str:
        return ('Raise ' if any(player.bet for player in self.game.players) else 'Bet ') + str(self.__amount)

    def _verify(self) -> None:
        super()._verify()

        max_bet: int = max(player.bet for player in self.game.players)

        if not ((max_bet + self.game.environment._max_delta <= self.__amount <= self.actor.total or
                 max_bet < self.__amount == self.actor.total) and
                sum(player.relevant for player in self.game.players) > 1):
            raise ValueError('The supplied raise or bet size is not allowed')


class RoundAction(PokerNatureAction):
    """RoundAction is the class for round transitions and showdowns."""

    def act(self) -> None:
        super().act()

        self.game._round._close()

        if sum(not player.mucked for player in self.game.players) == 1:
            self.game._rounds.clear()
        else:
            self.game._rounds.pop(0)

        if self.game._round is not None:
            self.game._round._open()
            self.game._actor = self.game._round._opener
        else:
            if sum(not player.mucked for player in self.game.players) > 1:
                self.__show()

            self.__distribute()

            self.game._actor = None

    def __str__(self) -> str:
        return 'Next Street'

    def __show(self) -> None:
        players: Iterable[PokerPlayer] = filter(lambda player: not player.mucked,
                                                rotate(self.game.players, self.game.environment._aggressor.index))

        commitments: defaultdict[Hand, int] = defaultdict(lambda: 0)

        for player in players:
            for hand, commitment in commitments.items():
                if player.hand < hand and commitment > player.commitment:
                    player._muck()
                    break
                else:
                    commitments[player.hand] = max(commitments[player.hand], player.commitment)

    def __distribute(self) -> None:
        players: list[PokerPlayer] = list(filter(lambda player: not player.mucked,
                                                 rotate(self.game.players, self.game.environment._aggressor.index)))
        base: int = 0

        for base_player in sorted(players):
            side_pot: int = self.__side_pot(base, base_player)

            recipients: list[PokerPlayer] = list(filter(lambda player: player.hand == base_player.hand, players))

            for recipient in recipients:
                recipient._bet += side_pot // len(recipients)
            else:
                recipients[0]._bet += side_pot % len(recipients)

            base = max(base, base_player.commitment)

        self.game.environment._pot = 0

        for player in players:
            player._stack += player.bet
            player._bet = 0

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot: int = 0

        for player in self.game.players:
            if base < (entitlement := min(player.commitment, base_player.commitment)):
                side_pot += entitlement - base

        return side_pot
