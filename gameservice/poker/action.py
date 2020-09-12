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

        if not (isinstance(amount, int) and (game.min_raise <= amount <= player.total or
                                             max(game.players.bets) < amount == player.total)):
            raise InvalidActionArgumentException

        self.amount = amount

    @property
    def label(self):
        return f"{'Raise' if max(self.game.players.bets) else 'Bet'} {self.amount}"

    def act(self):
        super().act()

        self.game.aggressor = self.player
        self.game.min_raise = self.amount + self.amount - max(self.game.players.bets)

        self.player.stack -= self.amount - self.player.bet
        self.player.bet = self.amount

        self.game.player = self.game.players.next_relevant(self.player)


class Continue(PokerPlayerAction):
    @property
    def label(self):
        return "Check" if max(self.game.players.bets) == self.player.bet else \
            f"Call {min(max(self.game.players.bets) - self.player.bet, self.player.stack)}"

    def act(self):
        super().act()

        amount = min(max(self.game.players.bets) - self.player.bet, self.player.stack)

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
        super().act()

        self.player.muck()

        if self.game.num_players - self.game.players.num_mucked == 1:
            self.stop_betting()
            self.game.results[None].extend(player for player in self.game.players if not player.mucked)
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
        super().act()

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
        return f"Peel {', '.join(self.game.deck.peak(self.num_cards))}"

    def act(self):
        super().act()

        self.game.context.board.extend(self.game.deck.draw(self.num_cards))
        self.start_betting()


class Showdown(PokerNatureAction):
    @property
    def label(self):
        return "Showdown"

    def act(self):
        super().act()

        if not self.game.chance_players:
            self.game.chance_players = []

            for i in range(self.game.players.index(self.game.aggressor),
                           self.game.players.index(self.game.aggressor) + len(self.game.players)):
                if not self.game.players[i % len(self.game.players)].mucked:
                    self.game.chance_players.append(self.game.players[i % len(self.game.players)])

        chance_player = self.game.chance_players.pop(0)

        for hand, players in self.game.results.items():
            if hand < chance_player.hand and max(player.commitment for player in players) >= chance_player.commitment:
                chance_player.muck()
                break
        else:
            self.game.results[chance_player.hand].append(chance_player)
            chance_player.expose()

        if not self.game.chance_players:
            self.game.street = None


class Distribute(PokerNatureAction):
    @property
    def label(self):
        return "Distribute"

    def act(self):
        super().act()

        distributed = 0

        while self.game.context.pot:
            cur_hand = min(self.game.results)
            players = self.game.results[cur_hand]
            min_player = min(players, key=lambda player: player.commitment)

            entitlement = min_player.commitment
            distribution = 0

            for player in self.game.players:
                if distributed < min(entitlement, player.commitment):
                    distribution += min(entitlement, player.commitment) - distributed

            players[0].bet += distribution % len(players)

            for player in players:
                player.bet += distribution // len(players)

            self.game.context.pot -= distribution
            distributed = entitlement

            players.remove(min_player)

            if not players:
                self.game.results.pop(cur_hand)

        for player in self.game.players:
            player.stack += player.bet
            player.bet = 0

        self.game.player = None
