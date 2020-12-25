"""
This module defines poker players in gameservice.
"""
from .actions import AggressiveAction, PassiveAction, ShowdownAction, StreetAction, SubmissiveAction
from .infosets import PokerInfoSet
from ..game import ActionException, Nature, Player


class PokerPlayer(Player):
    """
    This is a class that represents poker players.
    """

    def __init__(self, game):
        super().__init__(game)

        self.stack = 0
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
                actions.append(SubmissiveAction(self))
            except ActionException:
                pass

            actions.append(PassiveAction(self))

            for amount in self.game.limit.bet_amounts(self):
                actions.append(AggressiveAction(self, amount))

        return actions

    @property
    def info_set(self):
        return PokerInfoSet(self)

    @property
    def mucked(self):
        """
        :return: a boolean value of whether or not the poker player has mucked
        """
        return self.hole_cards is None

    @property
    def commitment(self):
        """
        :return: the amount the poker player has put into the pot
        """
        return -self.payoff

    @property
    def total(self):
        """
        :return: the sum of the bet and the stack of the poker player
        """
        return self.stack + self.bet

    @property
    def effective_stack(self):
        """
        Finds the effective stack of the poker player.

        The effective stack denotes how much a player can lose in a pot.

        :return: the effective stack of the poker player
        """
        return min(sorted(player.total for player in self.game.players)[-2], self.total)

    @property
    def relevant(self):
        """
        Finds the relevancy of the poker player.

        A poker player is relevant if he/she can make a bet/raise and there is at least one opponent who can call.

        :return: the relevancy of the poker player
        """
        return not self.mucked and self.stack > 0 and self.effective_stack > 0

    @property
    def hand(self):
        """
        :return: the hand of the poker player if any hand is made else None
        """
        return self.game.evaluator.hand(self.hole_cards, self.game.environment.board)

    def __next__(self):
        player = super().__next__()

        while not player.relevant and player is not self.game.environment.aggressor:
            player = Player.__next__(player)

        return self.game.nature if player is self.game.environment.aggressor else player


class PokerNature(Nature):
    """
    This is a class that represents poker natures.
    """

    @property
    def actions(self):
        if self.game.player is self:
            return [ShowdownAction(self) if self.game.street is None else StreetAction(self)]
        else:
            return []

    @property
    def info_set(self):
        return PokerInfoSet(self)
