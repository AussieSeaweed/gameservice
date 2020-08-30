from ..poker.action import StreetAction


class PreFlop(StreetAction):
    def __init__(self, game, player, num_cards):
        super().__init__(game, player)

        self.num_cards = num_cards

    @property
    def label(self):
        return f"Deal {self.num_cards} cards"

    def act(self):
        if not self.player.chance_players:
            self.player.chance_players = [player for player in self.game.players if not player.mucked]

        chance_player = self.player.chance_players[0]

        chance_player.cards.extend(
            chance_player.Card(card_str, False) for card_str in self.game.deck.draw(self.num_cards))

        self.player.chance_players.pop(0)

        if not self.player.chance_players:
            self.begin_betting(self.game.players[1] if self.game.num_players == 2 else self.game.players[2])
