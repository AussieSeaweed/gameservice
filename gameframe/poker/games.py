from abc import ABC
from itertools import zip_longest

from gameframe.poker.actors import PokerNature, PokerPlayer
from gameframe.poker.environments import PokerEnvironment
from gameframe.poker.exceptions import InsufficientPlayerCountException, InvalidBlindConfigurationException
from gameframe.poker.limits import NoLimit
from gameframe.poker.rounds import BettingRound
from gameframe.poker.utils import StandardDeck, StandardEvaluator
from gameframe.sequential import SequentialGame


class PokerGame(SequentialGame, ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, deck, evaluator, rounds, limit, ante, blinds, starting_stacks, laziness=False):
        super().__init__(
            PokerEnvironment(self),
            PokerNature(self),
            (PokerPlayer(self) for _ in range(len(starting_stacks))),
            None,
        )

        self._deck = deck
        self._evaluator = evaluator

        self._rounds = [None] + list(rounds)
        self._limit = limit

        self.__ante = ante
        self.__blinds = blinds
        self.__starting_stacks = tuple(starting_stacks)

        self.__laziness = laziness

        if len(self.players) < 2:
            raise InsufficientPlayerCountException()
        elif blinds != sorted(blinds) and len(blinds) != 2:
            raise InvalidBlindConfigurationException()

        self._setup()

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
    def is_lazy(self):
        """
        :return: True if this poker game is lazy, else False
        """
        return self.__laziness

    @property
    def _round(self):
        return self._rounds[0] if self._rounds else None

    @property
    def _information(self):
        return {
            **super()._information,
            'ante': self.ante,
            'blinds': self.blinds,
            'starting_stacks': self.starting_stacks,
        }

    def _setup(self):
        for player, blind in zip_longest(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds,
                                         fillvalue=0):
            player._commitment = min(self.ante + blind, player.starting_stack)

        self.environment._requirement = self.ante


class HoldEmGame(PokerGame, ABC):
    """HoldEmGame is the abstract base class for all hold'em games."""

    def __init__(self, deck, evaluator, hole_card_count, board_card_counts, limit, ante, blinds, starting_stacks,
                 laziness=False):
        super().__init__(
            deck, evaluator, [BettingRound(self, 0, [False] * hole_card_count)] + list(map(
                lambda board_card_count: BettingRound(self, board_card_count, []), board_card_counts,
            )), limit, ante, blinds, starting_stacks, laziness
        )


class TexasHoldEmGame(HoldEmGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, laziness=False):
        super().__init__(StandardDeck(), StandardEvaluator(), 2, [3, 1, 1], limit, ante, blinds, starting_stacks,
                         laziness)


class NoLimitTexasHoldEmGame(TexasHoldEmGame, ABC):
    """NoLimitTexasHoldEmGame is the abstract base class for all no-limit texas hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, laziness=False):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, laziness)
