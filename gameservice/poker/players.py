from .actions import PokerAggressiveAction, PokerPassiveAction, PokerShowdownAction, PokerStreetAction, \
    PokerSubmissiveAction
from .infosets import PokerInfoSet
from ..game import ActionException, Nature, Player


class PokerPlayer(Player):
    def __init__(self, game, index):
        super().__init__(game)

        self.stack = game.starting_stacks[index]
        self.bet = 0
        self.hole_cards = []

    @property
    def payoff(self):
        return self.stack - self.game.starting_stacks[self.index]

    @property
    def actions(self):
        actions = []

        if self.game.player is self:
            try:
                actions.append(PokerSubmissiveAction(self))
            except ActionException:
                pass

            actions.append(PokerPassiveAction(self))

            for amount in self.game.limit.bet_amounts(self):
                actions.append(PokerAggressiveAction(self, amount))

        return actions

    @property
    def info_set(self):
        return PokerInfoSet(self)

    @property
    def mucked(self):
        return self.hole_cards is None

    @property
    def commitment(self):
        return -self.payoff

    @property
    def total(self):
        return self.stack + self.bet

    @property
    def effective_stack(self):
        return min(sorted(player.total for player in self.game.players)[-2], self.total)

    @property
    def relevant(self):
        return not self.mucked and self.stack > 0 and self.effective_stack > 0

    @property
    def hand(self):
        return self.game.evaluator.hand(self.hole_cards, self.game.environment.board)

    def __next__(self):
        player = super().__next__()

        while not player.relevant and player is not self.game.environment.aggressor:
            player = Player.__next__(player)

        return self.game.nature if player is self.game.environment.aggressor else player


class PokerNature(Nature):
    @property
    def actions(self):
        if self.game.player is self:
            return [PokerShowdownAction(self) if self.game.street is None else PokerStreetAction(self)]
        else:
            return []

    @property
    def info_set(self):
        return PokerInfoSet(self)
