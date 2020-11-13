from .pokeraction import PokerSubmissiveAction, PokerPassiveAction, PokerAggressiveAction, PokerStreetAction, \
    PokerShowdownAction
from .pokerinfoset import PokerInfoSet
from .pokerutils import PokerHand
from ..game import Player, Nature


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
            if self.bet < max(self.game.bets):
                actions.append(PokerSubmissiveAction(self))

            actions.append(PokerPassiveAction(self))

            if sum(player.relevant for player in self.game.players) > 1:
                for amount in self.game.limit.bet_amounts(self):
                    actions.append(PokerAggressiveAction(self, amount))

        return actions

    @property
    def info_set(self):
        return PokerInfoSet(self)

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
        return self.hole_cards is not None and self.stack > 0 and self.effective_stack > 0

    @property
    def hand(self):
        return PokerHand(self.game.evaluator.hand_rank(self.hole_cards, self.game.board))

    def __next__(self):
        player = Player.__next__(self)

        while not player.relevant and player is not self.game.aggressor:
            player = Player.__next__(player)

        return self.game.nature if player is self.game.aggressor else player


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
