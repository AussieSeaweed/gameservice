from abc import ABC, abstractmethod

from gameframe.poker.actions import BetRaiseAction, CheckCallAction, FoldAction
from gameframe.poker.utils import HoleCard


class Round(ABC):
    """Round is the abstract base class for all rounds."""

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """
        :return: the game of this round
        """
        return self.__game

    @property
    @abstractmethod
    def actions(self):
        """
        :return: the actions of this round
        """
        pass

    @property
    @abstractmethod
    def opener(self):
        """
        :return: the opener of this round
        """
        pass

    @property
    @abstractmethod
    def is_betting(self):
        """
        :return: True if this round is a betting round, else False
        """
        pass

    @abstractmethod
    def open(self):
        """Opens this round.

        :return: None
        """
        pass

    @abstractmethod
    def close(self):
        """Closes this round.

        :return: None
        """
        pass


class BettingRound(Round, ABC):
    """BettingRound is the class for betting rounds."""

    def __init__(self, game, board_card_count, hole_card_statuses):
        super().__init__(game)

        self.__board_card_count = board_card_count
        self.__hole_card_statuses = hole_card_statuses

    @property
    def actions(self):
        actions = [FoldAction(self.game.actor), CheckCallAction(self.game.actor)]

        if self.game.is_lazy:
            bet_amounts = sorted({self.game._limit.min_amount, self.game._limit.max_amount})
        else:
            bet_amounts = range(self.game._limit.min_amount, self.game._limit.max_amount + 1)

        actions.extend(map(lambda amount: BetRaiseAction(self.game.actor, amount), bet_amounts))

        return list(filter(lambda action: action.is_applicable, actions))

    @property
    def opener(self):
        opener = min(self.game.players, key=lambda player: (player.bet, player.index))

        for opener in self.game.players[opener.index:] + self.game.players[:opener.index]:
            if opener._is_relevant:
                return opener
        else:
            return self.game.nature

    @property
    def is_betting(self):
        return True

    def open(self):
        self.game.environment._board_cards.extend(self.game._deck.draw(self.__board_card_count))

        for player in self.game.players:
            if not player.is_mucked:
                player._hole_cards.extend(map(
                    lambda args: HoleCard(*args),
                    zip(self.game._deck.draw(len(self.__hole_card_statuses)), self.__hole_card_statuses)
                ))

        if not self.opener.is_nature:
            self.game.environment._max_delta = max(self.game.ante, max(self.game.blinds))
            self.game.environment._aggressor = self.opener

    def close(self):
        self.game.environment._max_delta = None
        self.game.environment._requirement = max(player._commitment for player in self.game.players)
