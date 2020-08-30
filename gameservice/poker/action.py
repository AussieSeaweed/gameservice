from abc import ABC

from gameservice.exceptions import InvalidActionArgumentException, InvalidActionException, NatureException
from gameservice.sequential.action import SequentialAction


class PokerPlayerAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if player.nature:
            raise NatureException

    def finish_betting(self):
        self.game.context.pot += sum(self.game.players.bets)

        for player in self.game.players:
            player.bet = 0

        self.game.player = self.game.players.nature
        self.game.street += 1


class StreetAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if not player.nature:
            raise NatureException

    def begin_betting(self, first_player=None):
        try:
            self.game.player = first_player if first_player is not None else next(
                player for player in self.game.players if player.relevant)
            self.game.aggressor = self.game.player
            self.game.min_raise = max(max(self.game.players.bets) * 2, self.game.bb)
        except StopIteration:
            self.game.street += 1


class Put(PokerPlayerAction):
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
        self.game.min_raise = self.amount + self.amount - max(self.game.players.bets)

        self.player.stack -= self.amount - self.player.bet
        self.player.bet = self.amount

        self.game.player = self.game.players.next_relevant(self.player)
        pass


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
            self.finish_betting()


class Surrender(PokerPlayerAction):
    def __init__(self, game, player):
        super().__init__(game, player)

        if max(game.players.bets) == player.bet:
            raise InvalidActionException

    @property
    def label(self):
        return "Fold"

    def act(self):
        self.player.muck()

        if self.game.num_players - self.game.players.num_mucked == 1:
            self.finish_betting()
            self.game.winners = [player for player in self.game.players if not player.mucked]
            self.game.street = None
        else:
            self.game.player = self.game.players.next_relevant(self.player)

            if self.game.player.nature or self.game.player == self.game.aggressor:
                self.finish_betting()


class Peel(StreetAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def label(self):
        return "Peel"

    def act(self):
        self.game.context.board.extend(self.game.deck.draw(self.num_cards))
        self.begin_betting()


class Showdown(StreetAction):
    @property
    def label(self):
        return "Showdown"

    def act(self):
        if not self.player.chance_players:
            self.player.chance_players = [player for player in self.game.players if not player.mucked]

            index = 0

            for i in range(len(self.player.chance_players)):
                if self.player.chance_players[i] is self.game.aggressor:
                    index = i
                    break

            self.player.chance_players = self.player.chance_players[index:] + self.player.chance_players[:index]

        chance_player = self.player.chance_players[0]

        if self.game.winning_hand is None or chance_player.hand < self.game.winning_hand:
            self.game.winning_hand = chance_player.hand
            self.game.winners = [chance_player]
            chance_player.expose()
        elif chance_player.hand == self.game.winning_hand:
            self.game.winners.append(chance_player)
            chance_player.expose()
        else:
            chance_player.muck()

        self.player.chance_players.pop(0)

        if not self.player.chance_players:
            self.game.street = None


class Distribute(StreetAction):
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
