from abc import ABC, abstractmethod
from itertools import zip_longest

from gameframe.poker.environments import PokerEnvironment
from gameframe.poker.players import PokerNature, PokerPlayer
from gameframe.utils.decks import StandardDeck
from gameframe.utils.evaluators import GreekHoldEmEvaluator, OmahaHoldEmEvaluator, StandardEvaluator
from gameframe.sequential import SequentialGame


class PokerGame(SequentialGame, ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self):
        super().__init__()

        if not len(self.starting_stacks) > 1:
            raise ValueError('Poker is played by more than 2 players')

        self._deck = self._create_deck()
        self._evaluator = self._create_evaluator()

        self._setup()

    @property
    @abstractmethod
    def ante(self):
        """
        :return: the ante of the poker game
        """
        pass

    @property
    @abstractmethod
    def blinds(self):
        """
        :return: the blinds of the poker game
        """
        pass

    @property
    @abstractmethod
    def starting_stacks(self):
        """
        :return: the starting stacks of the poker game
        """
        pass

    def _setup(self):
        blinds = reversed(self.blinds) if len(self.players) == 2 else self.blinds

        for player, starting_stack, blind in zip_longest(self.players, self.starting_stacks, blinds):
            player.stack = starting_stack

            ante = min(self.ante, player.stack)

            player.stack -= ante
            self.environment.pot += ante

            if blind is not None:
                blind = min(blind, player.stack)

                player.stack -= blind
                player.bet += blind

    def _create_environment(self):
        return PokerEnvironment(self)

    def _create_nature(self):
        return PokerNature(self)

    def _create_players(self):
        return [PokerPlayer(self) for _ in range(len(self.starting_stacks))]

    @property
    def _information(self):
        return {
            **super()._information,
            'ante': self.ante,
            'blinds': self.blinds,
            'starting_stacks': self.starting_stacks,
        }

    @property
    def _initial_player(self):
        return self.nature

    @abstractmethod
    def _create_deck(self):
        pass

    @abstractmethod
    def _create_evaluator(self):
        pass


class CommunityCardGame(PokerGame, ABC):
    """CommunityCardGame is the abstract base class for all community card games."""
    pass


class TexasHoldEmGame(CommunityCardGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return StandardEvaluator()


class OmahaHoldEmGame(CommunityCardGame, ABC):
    """OmahaHoldEmGame is the abstract base class for all omaha hold'em games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return OmahaHoldEmEvaluator()


class GreekHoldEmGame(CommunityCardGame, ABC):
    """GreekHoldEmGame is the abstract base class for all greek hold'em games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return GreekHoldEmEvaluator()


class DrawGame(PokerGame, ABC):
    """DrawGame is the abstract base class for all draw games."""
    pass


class FiveCardDraw(PokerGame, ABC):
    """FiveCardDraw is the abstract base class for all five card draw games."""

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return StandardEvaluator()
