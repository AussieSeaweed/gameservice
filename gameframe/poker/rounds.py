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

        if self.game.lazy:
            bet_amounts = sorted({self.game.limit.min_amount, self.game.limit.max_amount})
        else:
            bet_amounts = range(self.game.limit.min_amount, self.game.limit.max_amount + 1)

        actions.extend(map(lambda amount: BetRaiseAction(self.game.actor, amount), bet_amounts))

        return list(filter(lambda action: action.applicable, actions))

    @property
    def opener(self):
        opener = min(self.game.players, key=lambda player: (player.bet, player.index))

        for player in self.game.players[opener.index:] + self.game.players[:opener.index]:
            if player.relevant:
                return player
        else:
            return self.game.nature

    @property
    def is_betting(self):
        return True

    def open(self):
        self.game.environment.board_cards.extend(self.game.deck.draw(self.__board_card_count))

        for player in self.game.players:
            if not player.mucked:
                for hole_card, status in zip(self.game.deck.draw(len(self.__hole_card_statuses)),
                                             self.__hole_card_statuses):
                    player.hole_cards.append(HoleCard(hole_card, status))

        if not self.opener.nature:
            self.game.environment.aggressor = self.opener
            self.game.environment.max_delta = max(self.game.ante, max(self.game.blinds))

    def close(self):
        self.game.environment.max_delta = None

        for player in self.game.players:
            player.bet = 0
