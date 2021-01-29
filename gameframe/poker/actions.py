from abc import ABC
from collections import defaultdict



class BettingRoundAction(PokerAction, ABC):
    """BettingRoundAction is the abstract base class for all player actions in a betting round."""

    @property
    def is_applicable(self):
        return super().is_applicable and not self.game.actor.is_nature and self.game._round.is_betting


class FoldAction(BettingRoundAction):
    """FoldAction is the class for folds."""

    def __str__(self):
        return 'Fold'

    @property
    def is_applicable(self):
        return super().is_applicable and self.actor.bet < max(player.bet for player in self.game.players)

    def act(self):
        super().act()

        self.actor._muck()

        if sum(not player.is_mucked for player in self.game.players) == 1:
            self.game._actor = self.game.nature
        else:
            self.game._actor = next(self.actor)


class CheckCallAction(BettingRoundAction):
    """CheckCallAction is the class for checks and calls."""

    def __str__(self):
        return f'Call {self.amount}' if self.amount else 'Check'

    @property
    def amount(self):
        return min(self.actor.stack, max(player.bet for player in self.game.players) - self.actor.bet)

    def act(self):
        super().act()

        self.actor._commitment += self.amount
        self.game._actor = next(self.actor)


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
    def is_applicable(self):
        return super().is_applicable and \
               max(player._commitment for player in self.game.players) < self.actor.starting_stack and \
               any(player._is_relevant for player in self.game.players if player is not self.actor) and \
               self.game._limit.min_amount <= self.amount <= self.game._limit.max_amount

    def act(self):
        super().act()

        self.game.environment._aggressor = self.actor
        self.game.environment._max_delta = max(self.game.environment._max_delta,
                                               self.amount - max(player.bet for player in self.game.players))
        self.actor._commitment += self.amount - self.actor.bet
        self.game._actor = next(self.actor)


class ProgressiveAction(PokerAction):
    """ProgressiveAction is the class for round transitions and showdowns."""

    def __str__(self):
        return 'Progress'

    @property
    def is_applicable(self):
        return super().is_applicable and self.actor.is_nature

    def act(self):
        super().act()

        if self.game._round is not None:
            self.game._round.close()

        if sum(not player.is_mucked for player in self.game.players) == 1:
            self.game._rounds.clear()
        else:
            self.game._rounds.pop(0)

        if self.game._round is None:
            if sum(not player.is_mucked for player in self.game.players) > 1:
                self.__show()

            self.__distribute()
            self.game._actor = None
        else:
            self.game._round.open()
            self.game._actor = next(self.actor)

    def __show(self):
        index = 0 if self.game.environment._aggressor is None else self.game.environment._aggressor.index
        players = filter(lambda player: not player.is_mucked, self.game.players[index:] + self.game.players[:index])
        commitments = defaultdict(int)

        for player in players:
            for hand, commitment in commitments.items():
                if hand < player.hand and commitment >= player._commitment:
                    player._muck()
                    break
            else:
                commitments[player.hand] = max(commitments[player.hand], player._commitment)

                for card in player.hole_cards:
                    card._status = True

    def __distribute(self):
        players = list(filter(lambda player: not player.is_mucked, self.game.players))
        base = 0

        for base_player in sorted(players, key=lambda player: (player.hand, player._commitment)):
            side_pot = self.__side_pot(base, base_player)

            recipients = list(filter(lambda player: player.hand == base_player.hand, players))

            for recipient in recipients:
                recipient._revenue += side_pot // len(recipients)
            else:
                recipients[0]._revenue += side_pot % len(recipients)

            base = max(base, base_player._commitment)

    def __side_pot(self, base, base_player):
        side_pot = 0

        for player in self.game.players:
            entitlement = min(player._commitment, base_player._commitment)

            if base < entitlement:
                side_pot += entitlement - base

        return side_pot
