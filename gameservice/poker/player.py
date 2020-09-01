from gameservice.game.player import Player, Nature


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

        if index <= 1:
            blind = self.game.bb if index ^ (game.num_players == 2) else self.game.sb

            self.stack -= blind
            self.bet += blind

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
    def mucked(self):
        return self.cards is None

    @property
    def relevant(self):
        return not self.mucked and self.stack > 0

    @property
    def hand(self):
        return self.game.evaluate(self.game.context.board + [card.str_val for card in self.cards])

    @property
    def payoff(self):
        return self.stack - self.starting_stack


class PokerNature(Nature):
    def __init__(self, game):
        super().__init__(game)

        self.chance_players = None
