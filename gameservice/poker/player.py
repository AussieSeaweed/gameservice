from gameservice.game.player import Player


class PokerPlayer(Player):
    class Card:
        def __init__(self, str_val, exposed):
            self.str_val = str_val
            self.exposed = exposed

    def __init__(self, game, index):
        super().__init__(game)

        self.starting_stack = game.starting_stacks[index]

        self.cards = []
        self.stack = self.starting_stack
        self.bet = 0
        self.button = index == game.num_players - 1

    @property
    def public_info(self):
        return {
            **super().public_info,
            "cards": None if self.mucked else [card.str_val if card.exposed else None for card in self.cards],
            "stack": self.stack,
            "bet": self.bet,
            "button": self.button,
        }

    @property
    def private_info(self):
        return {
            **super().private_info,
            "cards": None if self.mucked else [card.str_val for card in self.cards],
        }

    def muck(self):
        self.cards = None

    def expose(self):
        for card in self.cards:
            card.exposed = True

    @property
    def total(self):
        return self.stack + self.bet

    @property
    def commitment(self):
        return self.starting_stack - self.stack

    @property
    def effective_stack(self):
        return min(sorted(player.total for player in self.game.players if not player.mucked)[-2], self.total)

    @property
    def mucked(self):
        return self.cards is None

    @property
    def relevant(self):
        return not self.mucked and self.stack > 0 and self.effective_stack > 0

    @property
    def hand(self):
        return self.game.evaluate(self.game.context.board + [card.str_val for card in self.cards])

    @property
    def payoff(self):
        return self.stack - self.starting_stack


class BlindedPokerPlayer(PokerPlayer):
    def __init__(self, game, index):
        super().__init__(game, index)

        if index <= 1:
            blind = self.game.bb if index ^ (game.num_players == 2) else self.game.sb

            self.stack -= blind
            self.bet += blind
