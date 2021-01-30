from abc import ABC
from collections import defaultdict
from typing import DefaultDict, Optional

from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.rounds import BettingRound
from gameframe.poker.utils import Hand
from gameframe.utils import rotate


class BettingAction(PokerAction[PokerPlayer], ABC):
    """BettingRoundAction is the abstract base class for all player actions in a betting round."""

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self._game.env.actor, PokerPlayer) \
               and isinstance(self._game.env._round, BettingRound)


class FoldAction(BettingAction):
    """FoldAction is the class for folds."""

    def __str__(self) -> str:
        return 'Fold'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and self._actor.bet < max(player.bet for player in self._game.players)

    def act(self) -> None:
        super().act()

        self._actor._muck()

        if sum(not player.is_mucked for player in self._game.players) == 1:
            self._game.env._actor = self._game.nature
        else:
            self._game.env._actor = next(self._actor)


class CheckCallAction(BettingAction):
    """CheckCallAction is the class for checks and calls."""

    def __str__(self) -> str:
        return f'Call {self.amount}' if self.amount else 'Check'

    @property
    def amount(self) -> int:
        return min(self._actor.stack, max(player.bet for player in self._game.players) - self._actor.bet)

    def act(self) -> None:
        super().act()

        self._actor._commitment += self.amount
        self._game.env._actor = next(self._actor)


class BetRaiseAction(BettingAction):
    """BetRaiseAction is the class for bets and raises."""

    def __init__(self, game: PokerGame, actor: PokerPlayer, amount: int):
        super().__init__(game, actor)

        self.__amount = amount

    def __str__(self) -> str:
        return ('Raise ' if any(player.bet for player in self._game.players) else 'Bet ') + str(self.amount)

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and \
               max(player._commitment for player in self._game.players) < self._actor._starting_stack and \
               any(player._is_relevant for player in self._game.players if player is not self._actor) and \
               self._game.env._limit.min_amount(self._actor) <= self.amount \
               <= self._game.env._limit.max_amount(self._actor)

    def act(self) -> None:
        super().act()

        self._game.env._aggressor = self._actor
        self._game.env._max_delta = max(self._game.env._max_delta,
                                        self.amount - max(player.bet for player in self._game.players))
        self._actor._commitment += self.amount - self._actor.bet
        self._game.env._actor = next(self._actor)


class ProgressiveAction(PokerAction[PokerNature]):
    """ProgressiveAction is the class for round transitions and showdowns."""

    def __str__(self) -> str:
        return 'Progress'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self._actor, PokerNature)

    def act(self) -> None:
        super().act()

        if self._game.env._round is not None:
            self._game.env._round.close()

        if sum(not player.is_mucked for player in self._game.players) == 1:
            self._game.env._rounds.clear()
        else:
            self._game.env._rounds.pop(0)

        if self._game.env._round is None:
            if sum(not player.is_mucked for player in self._game.players) > 1:
                self.__show()

            self.__distribute()
            self._game.env._actor = None
        else:
            self._game.env._round.open()
            self._game.env._actor = next(self._actor)

    def __show(self) -> None:
        index = 0 if self._game.env._aggressor is None else self._game.players.index(self._game.env._aggressor)
        players = filter(lambda p: not p.is_mucked, rotate(self._game.players, index))
        commitments: DefaultDict[Hand, int] = defaultdict(int)

        for player in players:
            for hand, commitment in commitments.items():
                if hand < player.hand and commitment >= player._commitment:
                    player._muck()
                    break
            else:
                if player.hand is not None:
                    commitments[player.hand] = max(commitments[player.hand], player._commitment)

                if player.hole_cards is not None:
                    for card in player.hole_cards:
                        card._status = True

    def __distribute(self) -> None:
        players = list(filter(lambda player: not player.is_mucked, self._game.players))
        base = 0

        for base_player in sorted(players, key=lambda player: (player.hand, player._commitment)):
            side_pot = self.__side_pot(base, base_player)

            recipients = list(filter(lambda player: player.hand == base_player.hand, players))

            for recipient in recipients:
                recipient._revenue += side_pot // len(recipients)
            else:
                recipients[0]._revenue += side_pot % len(recipients)

            base = max(base, base_player._commitment)

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot = 0

        for player in self._game.players:
            entitlement = min(player._commitment, base_player._commitment)

            if base < entitlement:
                side_pot += entitlement - base

        return side_pot
