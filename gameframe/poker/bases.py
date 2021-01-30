from __future__ import annotations

from abc import ABC
from itertools import zip_longest
from typing import Iterator, MutableSequence, Optional, Sequence, TYPE_CHECKING, Union

from gameframe.game import Actor
from gameframe.poker.exceptions import BlindConfigException, PlayerCountException
from gameframe.poker.limits import Limit
from gameframe.poker.rounds import Round
from gameframe.game.bases import A
from gameframe.poker.utils import Card, Deck, Evaluator, Hand, HoleCard
from gameframe.sequential import SeqAction, SeqEnv, SeqGame


class PokerGame(SeqGame['PokerEnv', 'PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, deck: Deck, evaluator: Evaluator, rounds: Sequence[Round], limit: Limit, stacks: Sequence[int],
                 ante: int, blinds: Sequence[int]):
        nature = PokerNature(self)
        super().__init__(PokerEnv(self, nature, deck, evaluator, rounds, limit), nature,
                         [PokerPlayer(self, stack) for stack in range(len(stacks))])

        self._ante = ante
        self._blinds = blinds

        if len(self.players) < 2:
            raise PlayerCountException()
        elif blinds != sorted(blinds) and len(blinds) != 2:
            raise BlindConfigException()

        self._setup(ante, blinds)

    def _setup(self, ante: int, blinds: Sequence[int]) -> None:
        for player, blind in zip_longest(self.players, reversed(blinds) if len(self.players) == 2 else blinds,
                                         fillvalue=0):
            player._commitment = min(ante + blind, player._starting_stack)

        self.env._requirement = ante


class PokerEnv(SeqEnv[PokerGame, 'PokerNature', 'PokerPlayer']):
    """PokerEnv is the class for poker environments."""

    def __init__(self, game: PokerGame, actor: PokerNature, deck: Deck, evaluator: Evaluator, rounds: Sequence[Round],
                 limit: Limit):
        super().__init__(game, actor)

        self._deck = deck
        self._evaluator = evaluator
        self._rounds: MutableSequence[Optional[Round]] = list(rounds)
        self._limit = limit

        self._rounds.insert(0, None)

        self._aggressor: Optional[PokerPlayer] = None
        self._board_cards: MutableSequence[Card] = []
        self._max_delta = 0
        self._requirement = 0

    @property
    def board_cards(self) -> Sequence[Card]:
        """
        :return: the board cards of this poker environment
        """
        return tuple(self._board_cards)

    @property
    def pot(self) -> int:
        """
        :return: the pot of this poker environment
        """
        if self._game.is_terminal:
            return 0
        else:
            return sum(min(player._commitment, self._requirement) for player in self._game.players)

    @property
    def _round(self) -> Optional[Round]:
        return self._rounds[0] if self._rounds else None


class PokerNature(Actor[PokerGame], Iterator[Union['PokerNature', 'PokerPlayer']]):
    """PokerNature is the class for poker natures."""

    def __next__(self) -> Union[PokerNature, PokerPlayer]:
        if self._game.env._round is not None:
            return self._game.env._round.opener
        else:
            raise StopIteration

    @property
    def actions(self) -> Sequence[PokerAction[PokerNature]]:
        from gameframe.poker.actions import ProgressiveAction

        return [ProgressiveAction(self._game, self)] if self is self._game.env.actor else []

    def progress(self) -> None:
        """Progresses the poker game.

        :return: None
        """
        from gameframe.poker.actions import ProgressiveAction

        ProgressiveAction(self._game, self).act()


class PokerPlayer(Actor[PokerGame], Iterator[Union[PokerNature, 'PokerPlayer']]):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame, starting_stack: int):
        super().__init__(game)

        self._starting_stack = starting_stack
        self._commitment = 0
        self._revenue = 0
        self._hole_cards: Optional[MutableSequence[HoleCard]] = []

    def __next__(self) -> Union[PokerNature, PokerPlayer]:
        player = super().__next__()

        if isinstance(player, PokerNature) or player is self._game.env._aggressor:
            return self._game.nature
        elif isinstance(player, PokerPlayer) and player._is_relevant:
            return player
        else:
            return next(player)

    @property
    def hole_cards(self) -> Optional[Sequence[HoleCard]]:
        """
        :return: the hole cards of this poker player
        """
        return None if self._hole_cards is None else tuple(self._hole_cards)

    @property
    def bet(self) -> int:
        """
        :return: the bet of this poker player
        """
        return max(self._commitment - self._game.env._requirement, 0)

    @property
    def stack(self) -> int:
        """
        :return: the stack of this poker player
        """
        return self._revenue + self._starting_stack - self._commitment

    @property
    def effective_stack(self) -> int:
        """
        :return: the effective stack of this poker player
        """
        try:
            return min(sorted(player._starting_stack for player in self._game.players if not player.is_mucked)[-2],
                       self._starting_stack)
        except IndexError:
            return 0

    @property
    def hand(self) -> Optional[Hand]:
        """
        :return: the hand of this poker player
        """
        if self.hole_cards is None:
            return None
        else:
            return self._game.env._evaluator.hand(self.hole_cards, self._game.env.board_cards)

    @property
    def is_mucked(self) -> bool:
        """
        :return: True if this poker player has mucked his/her hand, else False
        """
        return self.hole_cards is None

    @property
    def actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        if self is self._game.env.actor and self._game.env._round is not None:
            return self._game.env._round.actions
        else:
            return []

    @property
    def _is_relevant(self) -> bool:
        return not self.is_mucked and self._commitment < self.effective_stack

    def fold(self) -> None:
        """Folds.

        :return: None
        """
        from gameframe.poker.actions import FoldAction

        FoldAction(self._game, self).act()

    def check_call(self) -> None:
        """Checks or calls.

        :return: None
        """
        from gameframe.poker.actions import CheckCallAction

        CheckCallAction(self._game, self).act()

    def bet_raise(self, amount: int) -> None:
        """Bets or Raises the amount.

        :param amount: the bet/raise amount
        :return: None
        """
        from gameframe.poker.actions import BetRaiseAction

        BetRaiseAction(self._game, self, amount).act()

    def _muck(self) -> None:
        """Mucks the hand of this poker player.

        :return: None
        """
        self._hole_cards = None


class PokerAction(SeqAction[PokerGame, A], ABC):
    """PokerAction is the abstract base class for all poker actions."""
    pass
