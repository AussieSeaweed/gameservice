from abc import ABC

from gameservice.exceptions import ActionArgumentException, PlayerTypeException
from gameservice.sequential.actions import SequentialAction


class PokerPlayerAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if player.nature:
            raise PlayerTypeException("Only player can apply this action")

    def close(self):
        self.game.context.pot += sum(self.game.players.bets)

        for player in self.game.players:
            player.bet = 0

        self.game.player = self.game.players.nature
        self.game.context.street += 1


class Put(PokerPlayerAction):
    def __init__(self, game, player, amount):
        super().__init__(game, player)

        if not (isinstance(amount, int) and self.game.players.num_relevant > 1 and
                (game.context.min_raise <= amount <= player.total or max(game.players.bets) < amount == player.total)):
            raise ActionArgumentException("Invalid bet/raise amount")

        self.amount = amount

    @property
    def name(self):
        return f"{'Raise' if max(self.game.players.bets) else 'Bet'} {self.amount}"

    def act(self):
        self.game.context.aggressor = self.player

        self.player.stack -= self.amount - self.player.bet
        self.player.bet = self.amount

        self.game.player = self.game.players.next_relevant(self.player)


class Continue(PokerPlayerAction):
    @property
    def name(self):
        return f"Call {self.amount}" if self.amount else "Check"

    def act(self):
        self.player.stack -= self.amount
        self.player.bet += self.amount

        self.game.player = self.game.players.next_relevant(self.player)

        if self.game.player.nature:
            self.close()

    @property
    def amount(self):
        return min(max(self.game.players.bets) - self.player.bet, self.player.stack)


class Surrender(PokerPlayerAction):
    def __init__(self, game, player):
        super().__init__(game, player)

        if max(game.players.bets) <= player.bet:
            raise ActionArgumentException("Cannot fold here")

    @property
    def name(self):
        return "Fold"

    def act(self):
        self.player.cards = None

        if self.game.num_players - self.game.players.num_mucked == 1:
            self.close()
            self.game.context.street = None
        else:
            self.game.player = self.game.players.next_relevant(self.player)

            if self.game.player.nature:
                self.close()
