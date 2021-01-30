from __future__ import annotations

from gameframe.game import Actor


class PokerNature(Actor):
    """PokerNature is the class for poker natures."""

    def __next__(self):
        return self.game._round.opener

    @property
    def actions(self):
        return [ProgressiveAction(self)] if self is self.game.actor else []

    @property
    def payoff(self):
        return 0

    def progress(self):
        """Progresses the poker game.

        :return: None
        """
        ProgressiveAction(self).act()


class PokerPlayer(Actor):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game):
        super().__init__(game)

        self._commitment = 0
        self._revenue = 0
        self._hole_cards = []

    def __next__(self):
        player = super().__next__()

        if player is self.game.environment._aggressor:
            return self.game.nature
        elif player._is_relevant:
            return player
        else:
            return next(player)

    @property
    def hole_cards(self):
        """
        :return: the hole cards of this poker player
        """
        return None if self._hole_cards is None else tuple(self._hole_cards)

    @property
    def bet(self):
        """
        :return: the bet of this poker player
        """
        return max(self._commitment - self.game.environment._requirement, 0)

    @property
    def stack(self):
        """
        :return: the stack of this poker player
        """
        return self._revenue + self.starting_stack - self._commitment

    @property
    def effective_stack(self):
        """
        :return: the effective stack of this poker player
        """
        try:
            return min(sorted(player.starting_stack for player in self.game.players if not player.is_mucked)[-2],
                       self.starting_stack)
        except IndexError:
            return 0

    @property
    def hand(self):
        """
        :return: the hand of this poker player
        """
        return self.game._evaluator.hand(self.hole_cards, self.game.environment.board_cards)

    @property
    def starting_stack(self):
        """
        :return: the starting stack of this poker player
        """
        return self.game.starting_stacks[self.index]

    @property
    def actions(self):
        return self.game._round.actions if self is self.game.actor and self.game._round is not None else []

    @property
    def payoff(self):
        return self._revenue - self._commitment

    @property
    def is_mucked(self):
        """
        :return: True if this poker player has mucked his/her hand, else False
        """
        return self.hole_cards is None

    @property
    def _is_relevant(self):
        return not self.is_mucked and self._commitment < self.effective_stack

    @property
    def _private_information(self):
        return {
            **super()._private_information,
            'hole_cards': self.hole_cards,
        }

    @property
    def _public_information(self):
        return {
            **super()._public_information,
            'bet': self.bet,
            'stack': self.stack,
            'hole_cards': None if self.is_mucked else tuple(map(
                lambda hole_card: hole_card if hole_card.status else None,
                self.hole_cards,
            )),
        }

    def fold(self):
        """Folds.

        :return: None
        """
        from gameframe.poker.actions import FoldAction

        FoldAction(self._game, self).act()

    def check_call(self):
        """Checks or calls.

        :return: None
        """
        from gameframe.poker.actions import CheckCallAction

        CheckCallAction(self).act()

    def bet_raise(self, amount):
        """Bets or Raises the amount.

        :param amount: the bet/raise amount
        :return: None
        """
        BetRaiseAction(self, amount).act()

    def _muck(self):
        """Mucks the hand of this poker player.

        :return: None
        """
        self._hole_cards = None
