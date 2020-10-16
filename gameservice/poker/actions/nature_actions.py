from abc import ABC
from collections import defaultdict

from gameservice.exceptions import PlayerTypeException
from gameservice.sequential.actions import SequentialAction


class PokerNatureAction(SequentialAction, ABC):
    def __init__(self, game, player):
        super().__init__(game, player)

        if not player.nature:
            raise PlayerTypeException("Only nature can apply this action")

    def open(self):
        self.game.player = self.opener

        if self.game.player.nature:
            self.game.context.street += 1
        else:
            self.game.context.aggressor = self.game.player

    @property
    def opener(self):
        try:
            return next(player for player in self.game.players if player.relevant)
        except StopIteration:
            return self.game.players.nature


class Deal(PokerNatureAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def name(self):
        return f"Deal {self.num_cards} cards"

    def act(self):
        for player in self.game.players:
            player.cards.extend(self.game.deck.draw(self.num_cards))

        self.open()


class Peel(PokerNatureAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def name(self):
        return f"Peel {', '.join(self.game.deck.peek(self.num_cards))}"

    def act(self):
        self.game.context.board.extend(self.game.deck.draw(self.num_cards))
        self.open()


class Showdown(PokerNatureAction):
    @property
    def name(self):
        return "Showdown"

    def act(self):
        player = self.game.context.aggressor
        commitments = defaultdict(lambda: 0)

        while player.mucked or player.exposed:
            if player.exposed:
                commitments[player.hand] = max(commitments[player.hand], player.commitment)

            player = self.game.players.next(player)

        for hand, commitment in commitments.items():
            if hand < player.hand and commitment >= player.commitment:
                player.cards = None
                break
        else:
            player.exposed = True

        if all(player.mucked or player.exposed for player in self.game.players):
            self.game.context.street = None


class Distribute(PokerNatureAction):
    @property
    def name(self):
        return "Distribute"

    def act(self):
        commitments = defaultdict(lambda: 0)

        for player in filter(lambda player: player.exposed, self.game.players):
            commitments[player.hand] = max(commitments[player.hand], player.commitment)

        players = []

        for player in filter(lambda player: not player.mucked, self.game.players):
            for hand, commitment in commitments.items():
                if hand < player.hand and commitment >= player.commitment:
                    break
            else:
                players.append(player)

        distributed = 0

        for min_player in sorted(players, key=lambda player: (player.hand, player.commitment)):
            side_pot = 0

            for player in self.game.players:
                if distributed < min(player.commitment, min_player.commitment):
                    side_pot += min(player.commitment, min_player.commitment) - distributed

            cur_players = list(filter(lambda player: player.hand == min_player.hand, players))

            cur_players[0].bet += side_pot % len(cur_players)

            for player in cur_players:
                player.bet += side_pot // len(cur_players)

            self.game.context.pot -= side_pot
            distributed = min_player.commitment

        for player in self.game.players:
            player.stack += player.bet
            player.bet = 0

        self.game.player = None
