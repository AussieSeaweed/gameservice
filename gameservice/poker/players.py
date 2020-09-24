from gameservice.game.players import Player, Nature


class PokerPlayer(Player):
    def __init__(self, game, index):
        super().__init__(game, index)

        self.cards = []
        self.stack = game.starting_stacks[index]
        self.bet = 0

        self.exposed = False

    @property
    def public_info(self):
        return {
            **super().public_info,
            "cards": self.cards if self.mucked or self.exposed else [None] * len(self.cards),
            "stack": self.stack,
            "bet": self.bet,

            "exposed": self.exposed,
        }

    @property
    def private_info(self):
        return {
            **super().private_info,
            "cards": self.cards,
        }

    @property
    def mucked(self):
        return self.cards is None

    @property
    def payoff(self):
        return self.stack - self.game.starting_stacks[self.index]

    @property
    def commitment(self):
        return self.game.starting_stacks[self.index] - self.stack

    @property
    def total(self):
        return self.stack + self.bet

    @property
    def effective_stack(self):
        return min(sorted(player.total for player in self.game.players if not player.mucked)[-2], self.total)

    @property
    def relevant(self):
        return not self.mucked and self.stack > 0 and self.effective_stack > 0

    @property
    def hand(self):
        return self.game.evaluate(self.game.context.board + self.cards)


class PokerNature(Nature):
    @property
    def payoff(self):
        return 0
