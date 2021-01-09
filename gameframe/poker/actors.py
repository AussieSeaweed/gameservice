from gameframe.game import Actor
from gameframe.poker.actions import BetRaiseAction, CheckCallAction, FoldAction, ProgressiveAction


class PokerNature(Actor):
    """PokerNature is the class for poker natures."""

    @property
    def actions(self):
        return [ProgressiveAction(self)] if self is self.game.actor else []

    @property
    def payoff(self):
        return 0

    def progress(self):
        ProgressiveAction(self).act()


class PokerPlayer(Actor):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game):
        super().__init__(game)

        self.bet = 0
        self.stack = 0
        self.__hole_cards = []

    def __next__(self):
        player = super().__next__()

        while not player.relevant and player is not self.game.environment.aggressor and player is not self:
            player = Actor.__next__(player)

        return self.game.nature if player is self.game.environment.aggressor or player is self else player

    @property
    def hole_cards(self):
        """
        :return: the hole cards of this poker player
        """
        return self.__hole_cards

    @property
    def commitment(self):
        """
        :return: the commitment of this poker player
        """
        return self.starting_stack - self.stack

    @property
    def effective_stack(self):
        """
        :return: the effective stack of this poker player
        """
        try:
            return min(sorted(player.total for player in self.game.players if not player.mucked)[-2], self.total)
        except IndexError:
            return 0

    @property
    def hand(self):
        """
        :return: the hand of this poker player
        """
        return self.game.evaluator.hand(self.hole_cards, self.game.environment.board_cards)

    @property
    def mucked(self):
        """
        :return: True if this poker player has mucked his/her hand, else False
        """
        return self.hole_cards is None

    @property
    def relevant(self):
        """
        :return: the relevancy of this poker player
        """
        return not self.mucked and self.stack > 0 and self.effective_stack > 0

    @property
    def starting_stack(self):
        """
        :return: the starting stack of this poker player
        """
        return self.game.starting_stacks[self.index]

    @property
    def total(self):
        """
        :return: the sum of the bet and the stack of this poker player
        """
        return self.bet + self.stack

    @property
    def actions(self):
        return self.game.round.actions if self is self.game.actor and self.game.round is not None else []

    @property
    def payoff(self):
        return -self.commitment

    @property
    def private_information(self):
        return {
            **super().private_information,
            'hole_cards': self.hole_cards,
        }

    @property
    def public_information(self):
        return {
            **super().public_information,
            'bet': self.bet,
            'stack': self.stack,
            'hole_cards': None if self.hole_cards is None else list(map(
                lambda hole_card: hole_card if hole_card.status else None,
                self.hole_cards,
            )),
        }

    def fold(self):
        """Folds.

        :return: None
        """
        FoldAction(self).act()

    def check_call(self):
        """Checks or calls.

        :return: None
        """
        CheckCallAction(self).act()

    def bet_raise(self, amount):
        """Bets or Raises the amount.

        :param amount: the bet/raise amount
        :return: None
        """
        BetRaiseAction(self, amount).act()

    def muck(self):
        """Mucks the hand of this poker player.

        :return: None
        """
        self.__hole_cards = None
