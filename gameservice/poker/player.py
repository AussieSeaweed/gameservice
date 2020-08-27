from gameservice.game.player import Player


class PokerPlayer(Player):
    class Card:
        def __init__(self, str_val, exposed):
            self.str_val = str_val
            self.exposed = exposed

    def __init__(self, game):
        super().__init__(game)

        self.cards = []
        self.stack = game.starting_stack
        self.bet = 0

    @property
    def public_info(self):
        return {
            **super().public_info,
            "cards": [card.str_val if card.exposed else None for card in self.cards],
            "stack": self.stack,
            "bet": self.bet,
        }

    @property
    def private_info(self):
        return {
            **super().private_info,
            "cards": [card.str_val for card in self.cards],
        }

    @property
    def mucked(self):
        return self.cards is None

    def expose(self):
        for card in self.cards:
            card.exposed = True
