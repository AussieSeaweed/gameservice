from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import zip_longest
from typing import MutableSequence, Optional, Sequence, TypeVar, Union

from gameframe.game import Actor
from gameframe.poker.exceptions import BlindException, IllegalStateException, PlayerCountException
from gameframe.poker.utils import Card, Deck, Evaluator, Hand, HoleCard
from gameframe.sequential import SeqAction, SeqEnv, SeqGame


class PokerEnv(SeqEnv):
    """PokerEnv is the class for poker environments."""

    def __init__(self, actor: Union[PokerNature, PokerPlayer], deck: Deck, evaluator: Evaluator,
                 stages: Sequence[Stage]):
        from gameframe.poker.stages import ShowdownStage

        super().__init__(actor)

        self._board_cards: MutableSequence[Card] = []
        self._aggressor: Optional[PokerPlayer] = None
        self._max_delta: int = 0
        self._pot = 0
        self._deck = deck
        self._evaluator = evaluator
        self._stages = list(stages) + [ShowdownStage(actor._game)]
        self._stage = stages[0]

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
        return self._pot


class PokerActor(Actor, ABC):
    def __init__(self, game: PokerGame):
        self._game = game


class PokerNature(PokerActor):
    """PokerNature is the class for poker natures."""

    @property
    def actions(self) -> Sequence[PokerAction[PokerNature]]:
        if self is self._game.env.actor:
            return self._game.env._stage.nature_actions
        else:
            return []

    def deal_hole_cards(self, *hole_cards: HoleCard) -> None:
        """Progresses the poker game.

        :return: None
        """
        from gameframe.poker.actions import HoleCardDealingAction

        HoleCardDealingAction(self._game, self, hole_cards).act()

    def deal_board_cards(self, *cards: Card) -> None:
        """Progresses the poker game.

        :return: None
        """
        from gameframe.poker.actions import BoardCardDealingAction

        BoardCardDealingAction(self._game, self, cards).act()

    def distribute(self) -> None:
        """Progresses the poker game.

        :return: None
        """
        from gameframe.poker.actions import DistributingAction

        DistributingAction(self._game, self).act()


class PokerPlayer(PokerActor):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame):
        super().__init__(game)

        self._bet = 0
        self._stack = 0
        self._hole_cards: Optional[MutableSequence[HoleCard]] = []

    @property
    def actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        if self is self._game.env.actor:
            return self._game.env._stage.player_actions
        else:
            return []

    @property
    def bet(self) -> int:
        """
        :return: the bet of this poker player
        """
        return self._bet

    @property
    def stack(self) -> int:
        """
        :return: the stack of this poker player
        """
        return self._stack

    @property
    def hole_cards(self) -> Optional[Sequence[Card]]:
        """
        :return: the hole cards of this poker player
        """
        return None if self._hole_cards is None else tuple(self._hole_cards)

    @property
    def effective_stack(self) -> int:
        """
        :return: the effective stack of this poker player
        """
        try:
            values = (player.stack + player.bet for player in self._game.players if not player.is_mucked)

            return min(sorted(values)[-2], self.stack)
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

    def showdown(self, force: bool = False) -> None:
        """Showdowns the player hole cards.

        :param force: force showdown
        :return: None
        """
        from gameframe.poker.actions import ShowdownAction

        ShowdownAction(self._game, self, force).act()

    def _muck(self) -> None:
        self._hole_cards = None


A = TypeVar('A', bound=Union[PokerNature, PokerPlayer], covariant=True)


class PokerGame(SeqGame[PokerEnv, PokerNature, PokerPlayer], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, deck: Deck, evaluator: Evaluator, stages: Sequence[Stage], ante: int, blinds: Sequence[int],
                 stacks: Sequence[int]):
        nature = PokerNature(self)

        super().__init__(PokerEnv(nature, deck, evaluator, stages), nature,
                         [PokerPlayer(self) for _ in range(len(stacks))])

        if len(self.players) < 2:
            raise PlayerCountException()
        elif blinds != sorted(blinds) and len(blinds) != 2:
            raise BlindException()

        self._setup(ante, blinds, stacks)

    def _setup(self, ante: int, blinds: Sequence[int], stacks: Sequence[int]) -> None:
        for player, blind, stack in zip_longest(self.players, reversed(blinds) if len(self.players) == 2 else blinds,
                                                stacks, fillvalue=0):
            player._stack = stack

            self.env._pot += min(ante, player._stack)
            player._stack -= min(ante, player._stack)

            player._bet = min(blind, player._stack)
            player._stack -= min(blind, player._stack)


class PokerAction(SeqAction[PokerEnv, PokerNature, PokerPlayer, A], ABC):
    """PokerPlayerAction is the abstract base class for all poker player actions."""
    pass


class Stage(ABC):
    def __init__(self, game: PokerGame):
        self.game = game

    @property
    def player(self) -> PokerPlayer:
        actor = self.game.env.actor

        if isinstance(actor, PokerPlayer):
            return actor
        else:
            raise IllegalStateException

    @property
    @abstractmethod
    def nature_actions(self) -> Sequence[PokerAction[PokerNature]]:
        pass

    @property
    @abstractmethod
    def player_actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        pass
