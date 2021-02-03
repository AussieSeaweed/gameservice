from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import zip_longest
from typing import Iterator, MutableSequence, Optional, Sequence, Union

from gameframe.game import ParamException
from gameframe.game.generics import A, Actor
from gameframe.poker.mixins import Openable
from gameframe.poker.utils import Card, Deck, Evaluator, Hand, HoleCard
from gameframe.poker.utils.cards import CardLike
from gameframe.sequential.generics import SeqAction, SeqEnv, SeqGame


class PokerGame(SeqGame['PokerEnv', 'PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, mid_stages: Sequence[MidStage], deck: Deck, evaluator: Evaluator, ante: int,
                 blinds: Sequence[int], stacks: Sequence[int]):
        nature = PokerNature(self)

        super().__init__(PokerEnv(self, nature, mid_stages, deck, evaluator, ante, blinds), nature,
                         [PokerPlayer(self, stack) for stack in stacks])

        if len(self.players) < 2:
            raise ParamException('Poker needs at least 2 players')
        elif any(a != b for a, b in zip_longest(blinds, sorted(blinds))):
            raise ParamException('Blinds have to be sorted')
        elif len(blinds) > len(self.players):
            raise ParamException('There are more blinds than players')


class PokerEnv(SeqEnv[PokerGame, 'PokerNature', 'PokerPlayer']):
    """PokerEnv is the class for poker environments."""

    def __init__(self, game: PokerGame, actor: PokerNature, mid_stages: Sequence[MidStage], deck: Deck,
                 evaluator: Evaluator, ante: int, blinds: Sequence[int]):
        from gameframe.poker.stages import SetupStage

        super().__init__(game, actor)

        self._stage: Stage = SetupStage(game)
        self._mid_stages = mid_stages

        self._deck = deck
        self._evaluator = evaluator
        self.__ante = ante
        self.__blinds = blinds

        self._board_cards: MutableSequence[Card] = []
        self._requirement = 0

    def __repr__(self) -> str:
        return f'PokerEnv({self.pot}, [' + ', '.join(map(str, self.board_cards)) + '])'

    @property
    def ante(self) -> int:
        """
        :return: the ante of this poker environment
        """
        return self.__ante

    @property
    def blinds(self) -> Sequence[int]:
        """
        :return: the blinds of this poker environment
        """
        return tuple(self.__blinds)

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
        if self.game.is_terminal:
            return 0
        else:
            return sum(min(player._commitment, self._requirement) for player in self.game.players)


class PokerNature(Actor[PokerGame]):
    """PokerNature is the class for poker natures."""

    def __repr__(self) -> str:
        return 'PokerNature'

    def setup(self) -> None:
        """Sets up the poker game of this nature.

        :return: None
        """
        from gameframe.poker.actions import SetupAction

        SetupAction(self.game, self).apply()

    def deal_player(self, player: PokerPlayer, *hole_cards: CardLike) -> None:
        """Deals the hole cards to a player.

        :param player: the player to deal to
        :param hole_cards: the hole cards to be dealt
        :return: None
        """
        from gameframe.poker.actions import HoleCardDealingAction

        HoleCardDealingAction(self.game, self, player, *hole_cards).apply()

    def deal_board(self, *cards: CardLike) -> None:
        """Deals the cards to the board.

        :param cards: the cards to be dealt
        :return: None
        """
        from gameframe.poker.actions import BoardCardDealingAction

        BoardCardDealingAction(self.game, self, *cards).apply()

    def distribute(self) -> None:
        """Distributes the pot.

        :return: None
        """
        from gameframe.poker.actions import DistributionAction

        DistributionAction(self.game, self).apply()


class PokerPlayer(Actor[PokerGame]):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame, stack: int):
        super().__init__(game)

        self._total = stack
        self._commitment = 0
        self._hole_cards: MutableSequence[HoleCard] = []
        self.__is_mucked = False

    def __repr__(self) -> str:
        if self.is_mucked:
            return f'PokerPlayer({self.bet}, {self.stack})'
        else:
            return f'PokerPlayer({self.bet}, {self.stack}, [' + ', '.join(map(str, self._hole_cards)) + '])'

    @property
    def bet(self) -> int:
        """
        :return: the bet of this poker player
        """
        return max(self._commitment - self.game.env._requirement, 0)

    @property
    def stack(self) -> int:
        """
        :return: the stack of this poker player
        """
        return self._total - self._commitment

    @property
    def hand(self) -> Hand:
        """
        :return: the hand of this poker player
        """
        return self.game.env._evaluator.hand(self._hole_cards, self.game.env.board_cards)

    @property
    def hole_cards(self) -> Optional[Sequence[HoleCard]]:
        """
        :return: the hole cards of this poker player
        """
        return None if self.is_mucked else tuple(self._hole_cards)

    @property
    def index(self) -> int:
        """
        :return: the index of this poker player
        """
        return self.game.players.index(self)

    @property
    def is_mucked(self) -> bool:
        """
        :return: True if this poker player has mucked his/her hand, else False
        """
        return self.__is_mucked

    @property
    def is_shown(self) -> bool:
        """
        :return: True if this poker player has shown his/her hand, else False
        """
        return all(hole_card.status for hole_card in self._hole_cards)

    @property
    def _effective_total(self) -> int:
        try:
            return min(sorted(player._total for player in self.game.players if not player.is_mucked)[-2], self._total)
        except IndexError:
            return 0

    @property
    def _is_relevant(self) -> bool:
        return not self.is_mucked and self._commitment < self._effective_total

    def fold(self) -> None:
        """Folds.

        :return: None
        """
        from gameframe.poker.actions import FoldAction

        FoldAction(self.game, self).apply()

    def check_call(self) -> None:
        """Checks or calls.

        :return: None
        """
        from gameframe.poker.actions import CheckCallAction

        CheckCallAction(self.game, self).apply()

    def bet_raise(self, amount: int) -> None:
        """Bets or Raises the amount.

        :param amount: the bet/raise amount
        :return: None
        """
        from gameframe.poker.actions import BetRaiseAction

        BetRaiseAction(self.game, self, amount).apply()

    def showdown(self, show: bool = False) -> None:
        """Showdowns the hand of this player if necessary or specified.

        :param show: a boolean value on whether or not to show regardless of necessity
        :return: None
        """
        from gameframe.poker.actions import ShowdownAction

        ShowdownAction(self.game, self, show).apply()

    def _muck(self) -> None:
        self.__is_mucked = True

        for card in self._hole_cards:
            card._status = False

    def _show(self) -> None:
        for card in self._hole_cards:
            card._status = True


class Stage(Iterator['Stage'], ABC):
    def __init__(self, game: PokerGame):
        self.game = game

    @property
    @abstractmethod
    def is_skippable(self) -> bool:
        pass


class OpenStage(Stage, Openable, ABC):
    @property
    @abstractmethod
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        pass

    def open(self) -> None:
        self.game.env._actor = self.opener


class MidStage(OpenStage, ABC):
    @property
    def is_skippable(self) -> bool:
        return sum(not player.is_mucked for player in self.game.players) == 1

    def __next__(self) -> Stage:
        from gameframe.poker.stages import DistributionStage

        if self is self.game.env._mid_stages[-1]:
            return DistributionStage(self.game)
        else:
            return self.game.env._mid_stages[self.index + 1]

    @property
    def index(self) -> int:
        return self.game.env._mid_stages.index(self)


class PokerAction(SeqAction[PokerGame, A], ABC):
    def apply(self) -> None:
        from gameframe.poker.mixins import Closeable, Openable

        super().apply()

        if self.game.env._stage.is_skippable:
            if isinstance(self.game.env._stage, Closeable):
                self.game.env._stage.close()

            self.game.env._stage = next(self.game.env._stage)

            while self.game.env._stage.is_skippable:
                self.game.env._stage = next(self.game.env._stage)

            if isinstance(self.game.env._stage, Openable):
                self.game.env._stage.open()
