from abc import ABC

from gameframe.poker.actors import PokerNature, PokerPlayer
from gameframe.poker.environments import PokerEnvironment
from gameframe.poker.exceptions import InsufficientPlayerCountException, InvalidBlindConfigurationException
from gameframe.poker.limits import NoLimit
from gameframe.poker.rounds import BettingRound
from gameframe.poker.utils import GreekHoldEmEvaluator, OmahaHoldEmEvaluator, StandardDeck, StandardEvaluator
from gameframe.sequential import SequentialGame


class PokerGame(SequentialGame, ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, rounds, deck, evaluator, limit, ante, blinds, starting_stacks, lazy):
        super().__init__(PokerEnvironment(self), PokerNature(self),
                         [PokerPlayer(self) for _ in range(len(starting_stacks))], None)

        self.__rounds = [None, *rounds]
        self.__deck = deck
        self.__evaluator = evaluator
        self.__limit = limit

        self.__ante = ante
        self.__blinds = blinds
        self.__starting_stacks = starting_stacks

        self.__lazy = lazy

        if len(self.players) < 2:
            raise InsufficientPlayerCountException()
        elif blinds != sorted(blinds):
            raise InvalidBlindConfigurationException()

        self._setup()

    @property
    def round(self):
        """
        :return: the current round of this poker game
        """
        return self.__rounds[0] if self.__rounds else None

    @property
    def rounds(self):
        """
        :return: the rounds of this poker game
        """
        return self.__rounds

    @property
    def deck(self):
        """
        :return: the deck of this poker game
        """
        return self.__deck

    @property
    def evaluator(self):
        """
        :return: the evaluator of this poker game
        """
        return self.__evaluator

    @property
    def limit(self):
        """
        :return: the limit of this poker game
        """
        return self.__limit

    @property
    def ante(self):
        """
        :return: the ante of this poker game
        """
        return self.__ante

    @property
    def blinds(self):
        """
        :return: the blinds of this poker game
        """
        return self.__blinds

    @property
    def starting_stacks(self):
        """
        :return: the starting stacks of this poker game
        """
        return self.__starting_stacks

    @property
    def lazy(self):
        """
        :return: True if this poker game is lazy else False
        """
        return self.__lazy

    @property
    def information(self):
        return {
            **super().information,
            'ante': self.ante,
            'blinds': self.blinds,
            'starting_stacks': self.starting_stacks,
        }

    def _setup(self):
        for player, stack in zip(self.players, self.starting_stacks):
            player.stack = stack

        for player in self.players:
            ante = min(self.ante, player.stack)

            player.stack -= ante

        for player, blind in zip(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds):
            blind = min(blind, player.stack)

            player.stack -= blind
            player.bet += blind


class HoldEmGame(PokerGame, ABC):
    """HoldEmGame is the abstract base class for all hold'em games."""

    def __init__(self, deck, evaluator, limit, hole_card_count, board_card_counts, ante, blinds, starting_stacks, lazy):
        super().__init__([BettingRound(self, 0, [False] * hole_card_count)] + list(map(
            lambda board_card_count: BettingRound(self, board_card_count, []), board_card_counts,
        )), deck, evaluator, limit, ante, blinds, starting_stacks, lazy)


class TexasHoldEmGame(HoldEmGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, lazy):
        super().__init__(StandardDeck(), StandardEvaluator(), limit, 2, [3, 1, 1], ante, blinds, starting_stacks, lazy)


class NoLimitTexasHoldEmGame(TexasHoldEmGame, ABC):
    """NoLimitTexasHoldEmGame is the abstract base class for all no-limit texas hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, lazy):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, lazy)


class GreekHoldEmGame(HoldEmGame, ABC):
    """GreekHoldEmGame is the abstract base class for all greek hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, lazy):
        super().__init__(StandardDeck(), GreekHoldEmEvaluator(), limit, 2, [3, 1, 1], ante, blinds, starting_stacks,
                         lazy)


class NoLimitGreekHoldEmGame(GreekHoldEmGame, ABC):
    """NoLimitGreekHoldEmGame is the abstract base class for all no-limit greek hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, lazy):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, lazy)


class OmahaHoldEmGame(HoldEmGame, ABC):
    """OmahaHoldEmGame is the abstract base class for all omaha hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, lazy):
        super().__init__(StandardDeck(), OmahaHoldEmEvaluator(), limit, 4, [3, 1, 1], ante, blinds, starting_stacks,
                         lazy)


class NoLimitOmahaHoldEmGame(OmahaHoldEmGame, ABC):
    """NoLimitOmahaHoldEmGame is the abstract base class for all no-limit omaha hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, lazy):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, lazy)
