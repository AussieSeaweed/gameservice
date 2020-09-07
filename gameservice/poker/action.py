from abc import ABC

from gameservice.exceptions import InvalidActionArgumentException, InvalidActionException, NatureException
from gameservice.sequential.action import SequentialAction


class PokerPlayerAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if player.nature:
            raise NatureException

    def stop_betting(self):
        self.game.context.pot += sum(self.game.players.bets)

        for player in self.game.players:
            player.bet = 0

        self.game.player = self.game.players.nature
        self.game.street += 1


class Put(PokerPlayerAction):
    def __init__(self, game, player, amount):
        super().__init__(game, player)

        if not (isinstance(amount, int) and (game.min_raise <= amount <= player.effective_stack or
                                             max(game.players.bets) < amount == player.effective_stack)):
            raise InvalidActionArgumentException

        self.amount = amount

    @property
    def label(self):
        return f"{'Raise' if max(self.game.players.bets) else 'Bet'} {self.amount}"

    def act(self):
        self.game.aggressor = self.player
        self.game.min_raise = self.amount + self.amount - max(self.game.players.bets)

        self.player.stack -= self.amount - self.player.bet
        self.player.bet = self.amount

        self.game.player = self.game.players.next_relevant(self.player)


class Continue(PokerPlayerAction):
    @property
    def label(self):
        return f"Call {max(self.game.players.bets) - self.player.bet}" if max(self.game.players.bets) != self.player.bet else "Check"

    def act(self):
        amount = max(self.game.players.bets) - self.player.bet

        self.player.stack -= amount
        self.player.bet += amount

        self.game.player = self.game.players.next_relevant(self.player)

        if self.game.player.nature or self.game.player == self.game.aggressor:
            self.stop_betting()


class Surrender(PokerPlayerAction):
    def __init__(self, game, player):
        super().__init__(game, player)

        if max(game.players.bets) <= player.bet:
            raise InvalidActionException

    @property
    def label(self):
        return "Fold"

    def act(self):
        self.player.muck()

        if self.game.num_players - self.game.players.num_mucked == 1:
            self.stop_betting()
            self.game.winners = [player for player in self.game.players if not player.mucked]
            self.game.street = None
        else:
            self.game.player = self.game.players.next_relevant(self.player)

            if self.game.player.nature or self.game.player == self.game.aggressor:
                self.stop_betting()


class PokerNatureAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if not player.nature:
            raise NatureException

    def start_betting(self):
        self.game.chance_players = None
        self.game.player = self.opener

        if self.game.player.nature:
            self.game.street += 1
        else:
            self.game.aggressor = self.game.player
            self.game.min_raise = max(max(self.game.players.bets) * 2, self.game.bb)

    @property
    def opener(self):
        try:
            return next(player for player in self.game.players if player.relevant)
        except StopIteration:
            return self.game.players.nature


class Deal(PokerNatureAction):
    def __init__(self, game, player, num_cards, exposed):
        super().__init__(game, player)

        self.num_cards = num_cards
        self.exposed = exposed

    @property
    def label(self):
        return f"Deal {self.num_cards} cards"

    def act(self):
        if not self.game.chance_players:
            self.game.chance_players = list(self.game.players)

        chance_player = self.game.chance_players.pop(0)

        chance_player.cards.extend(chance_player.Card(card_str, self.exposed) for card_str in
                                   self.game.deck.draw(self.num_cards))

        if not self.game.chance_players:
            self.start_betting()


class Peel(PokerNatureAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def label(self):
        return "Peel"

    def act(self):
        self.game.context.board.extend(self.game.deck.draw(self.num_cards))
        self.start_betting()


class Showdown(PokerNatureAction):
    @property
    def label(self):
        return "Showdown"

    def act(self):
        if not self.game.chance_players:
            self.game.chance_players = []

            for i in range(self.game.players.index(self.game.aggressor),
                           self.game.players.index(self.game.aggressor) + len(self.game.players)):
                if not self.game.players[i % len(self.game.players)].mucked:
                    self.game.chance_players.append(self.game.players[i % len(self.game.players)])

        chance_player = self.game.chance_players.pop(0)

        if self.game.winning_hand is None or chance_player.hand < self.game.winning_hand:
            self.game.winning_hand = chance_player.hand
            self.game.winners = [chance_player]
            chance_player.expose()
        elif chance_player.hand == self.game.winning_hand:
            self.game.winners.append(chance_player)
            chance_player.expose()
        else:
            chance_player.muck()

        if not self.game.chance_players:
            self.game.street = None


class Distribute(PokerNatureAction):
    @property
    def label(self):
        return "Distribute"

    def act(self):
        self.game.winners[0].stack += self.game.context.pot % len(self.game.winners)

        for winner in self.game.winners:
            winner.stack += self.game.context.pot // len(self.game.winners)

        self.game.context.pot = 0

        self.game.player = None
