from abc import ABC
from collections import defaultdict

from gameframe.sequential import SequentialAction


class PokerAction(SequentialAction, ABC):
    """PokerAction is the abstract base class for all poker actions."""

    @property
    def public(self):
        return True


class BettingRoundAction(PokerAction, ABC):
    """BettingRoundAction is the abstract base class for all player actions in a betting round."""

    @property
    def applicable(self):
        return super().is_applicable and not self.game.actor.is_nature and self.game.round.is_betting


class FoldAction(BettingRoundAction):
    """FoldAction is the class for folds."""

    def __str__(self):
        return 'Fold'

    @property
    def applicable(self):
        return super().applicable and self.actor.bet < max(player.bet for player in self.game.players)

    def act(self):
        super().act()

        self.actor.muck()

        if sum(not player.mucked for player in self.game.players) == 1:
            self.game.actor = self.game.nature
        else:
            self.game.actor = next(self.actor)


class CheckCallAction(BettingRoundAction):
    """CheckCallAction is the class for checks and calls."""

    def __str__(self):
        return f'Call {self.amount}' if self.amount else 'Check'

    @property
    def amount(self):
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self):
        super().act()

        amount = self.amount

        self.actor.stack -= amount
        self.actor.bet += amount

        self.game.actor = next(self.actor)


class BetRaiseAction(BettingRoundAction):
    """BetRaiseAction is the class for bets and raises."""

    def __init__(self, actor, amount):
        super().__init__(actor)

        self.__amount = amount

    def __str__(self):
        return ('Raise ' if any(player.bet for player in self.game.players) else 'Bet ') + str(self.amount)

    @property
    def amount(self):
        return self.__amount

    @property
    def applicable(self):
        return super().applicable and sum(player.relevant for player in self.game.players) > 1 and \
               max(player.bet for player in self.game.players) < self.actor.total and \
               self.game.limit.min_amount <= self.amount <= self.game.limit.max_amount

    def act(self):
        super().act()

        self.game.environment.max_delta = max(self.game.environment.max_delta,
                                              self.amount - max(player.bet for player in self.game.players))

        self.actor.stack -= self.amount - self.actor.bet
        self.actor.bet = self.amount

        self.game.environment.aggressor = self.actor
        self.game.actor = next(self.actor)


class ProgressiveAction(PokerAction):
    """ProgressiveAction is the class for round transitions and showdowns."""

    def __str__(self):
        return 'Progress'

    @property
    def applicable(self):
        return super().applicable and self.actor.nature

    def act(self):
        super().act()

        if self.game.round is not None:
            self.game.round.close()

        if sum(not player.mucked for player in self.game.players) == 1:
            self.game.rounds.clear()
        else:
            self.game.rounds.pop(0)

        if self.game.round is None:
            if sum(not player.mucked for player in self.game.players) > 1:
                self.__show()

            self.__distribute()
            self.game.actor = None
        else:
            self.game.round.open()
            self.game.actor = self.game.round.opener

    def __show(self):
        players = self.game.players

        if self.game.environment.aggressor is not None:
            players = players[self.game.environment.aggressor.index:] + players[:self.game.environment.aggressor.index]

        players = list(filter(lambda player: not player.mucked, players))

        commitments = defaultdict(int)

        for player in players:
            for hand, commitment in commitments.items():
                if hand < player.hand and commitment >= player.commitment:
                    player.muck()
                    break
            else:
                commitments[player.hand] = max(commitments[player.hand], player.commitment)

                for card in player.hole_cards:
                    card.status = True

    def __distribute(self):
        base = 0
        players = list(filter(lambda player: not player.mucked, self.game.players))

        for base_player in sorted(players, key=lambda player: (player.hand, player.commitment)):
            side_pot = self.__side_pot(base, base_player)

            recipients = list(filter(lambda player: player.hand == base_player.hand, players))

            for recipient in recipients:
                recipient.bet += side_pot // len(recipients)
            else:
                recipients[0].bet += side_pot % len(recipients)

            base = max(base, base_player.commitment)

        for player in self.game.players:
            if base < player.commitment:
                player.bet += player.commitment - base

            player.stack += player.bet
            player.bet = 0

    def __side_pot(self, base, base_player):
        side_pot = 0

        for player in self.game.players:
            entitlement = min(player.commitment, base_player.commitment)

            if base < entitlement:
                side_pot += entitlement - base

        return side_pot
