from abc import ABC

from ..exceptions import InvalidActionArgumentException, InvalidActionException
from ..sequential.action import SequentialAction


class AggressiveAction(SequentialAction):
    def __init__(self, game, player, amount):
        super().__init__(game, player)

        if not (isinstance(amount, int) and (game.min_raise <= amount <= player.total or
                                             max(game.players.bets) < amount == player.total)):
            raise InvalidActionArgumentException

        self.amount = amount

    @property
    def label(self):
        return f"{'Raise' if max(self.game.players.bets) else 'Bet'} {self.amount}"

    def act(self):
        self.game.aggressor = self.player
        self.game.min_raise = self.amount - max(self.game.players.bets)

        self.player.stack = self.amount - self.player.bet
        self.player.bet = self.amount


class PassiveAction(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return f"Call {max(self.game.players.bets) - self.player.bet}" if max(self.game.players.bets) else "Check"

    def act(self):
        self.player.stack -= max(self.game.players.bets) - self.player.bet
        self.player.bet = max(self.game.players.bets)


class YieldingAction(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

        if max(game.players.bets) == player.bet:
            raise InvalidActionException

    @property
    def label(self):
        return "Fold"

    def act(self):
        self.player.cards = None


class NewStreetAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

    def act(self):
        self.game.aggressor = self.game.players.next(self.player.target)
        self.game.min_raise = self.game.sb


class Deal(SequentialAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def label(self):
        return f"Deal {self.num_cards} cards"

    def act(self):
        if self.player.target is None:
            self.player.target = next(player for player in self.game.players if not player.mucked)

        self.player.target.cards.extend(self.player.target.Card(card_str, False) for card_str in
                                        self.game.deck.draw(self.num_cards))

        self.player.target = self.game.players.next(self.player.target)

        if self.player.target is self.game.aggressor:
            self.player.target = None
            self.game.next()


class Peel(SequentialAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def label(self):
        return "Peel"

    def act(self):
        self.game.context.board.extend(self.game.deck.draw(self.num_cards))
        self.game.player = next(player for player in self.game.players if not player.mucked)


class Showdown(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return "Showdown"

    def act(self):
        if self.player.target is None:
            self.player.target = self.game.aggressor

        if self.game.winning_hand is None or self.player.target.hand < self.game.winning_hand:
            self.game.winning_hand = self.player.target.hand
            self.game.winners = [self.player.target]
        elif self.player.target.hand == self.game.winning_hand:
            self.game.winners.append(self.player.target)
        else:
            self.player.target.muck()

        self.player.target = self.game.players.next(self.player.target)

        if self.player.target is self.game.aggressor:
            self.player.target = None

        self.game.next()


class Distribute(SequentialAction):
    def __init__(self, game, player):
        super().__init__(game, player)

    @property
    def label(self):
        return "Distribute"

    def act(self):
        if not self.game.winners:
            self.game.winners = [player for player in self.game.players if not player.mucked]

        self.game.winners[0].stack += self.game.context.pot % len(self.game.winners)

        for winner in self.game.winners:
            winner.stack += self.game.context.pot // len(self.game.winners)

        self.game.context.pot = 0
        self.game.player = None
