from __future__ import annotations

from abc import ABC
from typing import Iterator, MutableSequence, Optional, Sequence, TypeVar, Union, cast

from gameframe.game import Actor
from gameframe.poker.exceptions import BlindConfigException, PlayerCountException
from gameframe.poker.utils import Card, Deck, Evaluator, Hand, HoleCard
from gameframe.sequential import SeqAction, SeqEnv, SeqGame


class PokerGame(SeqGame['PokerEnv', 'PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, deck: Deck, evaluator: Evaluator, rounds: Sequence[BaseRound], ante: int, blinds: Sequence[int],
                 stacks: Sequence[int]):
        nature = PokerNature(self)

        super().__init__(PokerEnv(self, nature, deck, evaluator, rounds, ante, blinds), nature,
                         [PokerPlayer(self, stack) for stack in range(len(stacks))])

        if len(self.players) < 2:
            raise PlayerCountException()
        elif blinds != sorted(blinds) or len(blinds) != 2:
            raise BlindConfigException()


class PokerEnv(SeqEnv[PokerGame, 'PokerNature', 'PokerPlayer']):
    """PokerEnv is the class for poker environments."""

    def __init__(self, game: PokerGame, actor: PokerNature, deck: Deck, evaluator: Evaluator,
                 rounds: Sequence[BaseRound], ante: int, blinds: Sequence[int]):
        from gameframe.poker.rounds import SetupRound
        super().__init__(game, actor)

        self._deck = deck
        self._evaluator = evaluator
        self._rounds: Sequence[BaseRound] = rounds
        self.__ante = ante
        self.__blinds = blinds

        self._round: BaseRound = SetupRound(game)

        self._board_cards: MutableSequence[Card] = []
        self._aggressor: Optional[PokerPlayer] = game.players[0]
        self._max_delta = 0
        self._requirement = 0

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

    @property
    def actions(self) -> Sequence[PokerAction[PokerNature]]:
        from gameframe.poker.rounds import NatureRound

        if self is self.game.env.actor:
            return cast(NatureRound, self.game.env._round).actions
        else:
            return []

    def setup(self) -> None:
        """Sets up the poker game of this nature.

        :return: None
        """
        from gameframe.poker.actions import SetupAction

        SetupAction(self.game, self).act()

    def deal_player(self, hole_cards: Sequence[HoleCard]) -> None:
        """Deals the hole cards to a player.

        :param hole_cards: the hole cards to be dealt
        :return: None
        """
        from gameframe.poker.actions import HoleCardDealingAction

        HoleCardDealingAction(self.game, self, hole_cards).act()

    def deal_board(self, cards: Sequence[Card]) -> None:
        """Deals the cards to the board.

        :param cards: the cards to be dealt
        :return: None
        """
        from gameframe.poker.actions import BoardCardDealingAction

        BoardCardDealingAction(self.game, self, cards).act()

    def distribute(self) -> None:
        """Distributes the pot.

        :return: None
        """
        from gameframe.poker.actions import DistributionAction

        DistributionAction(self.game, self).act()


class PokerPlayer(Actor[PokerGame], Iterator[Union[PokerNature, 'PokerPlayer']]):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame, stack: int):
        super().__init__(game)

        self._total = stack
        self._commitment = 0
        self._hole_cards: MutableSequence[HoleCard] = []
        self.__is_mucked = False

    def __next__(self) -> Union[PokerNature, PokerPlayer]:
        player = self.game.players[(self.game.players.index(self) + 1) % len(self.game.players)]

        if player is self.game.env._aggressor:
            return self.game.nature
        elif player._is_relevant:
            return player
        else:
            return next(player)

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
    def effective_stack(self) -> int:
        """
        :return: the effective stack of this poker player
        """
        try:
            return min(sorted(player._total for player in self.game.players if not player.is_mucked)[-2], self._total)
        except IndexError:
            return 0

    @property
    def hand(self) -> Hand:
        """
        :return: the hand of this poker player
        """
        return self.game.env._evaluator.hand(self.hole_cards, self.game.env.board_cards)

    @property
    def hole_cards(self) -> Sequence[HoleCard]:
        """
        :return: the hole cards of this poker player
        """
        return None if self._hole_cards is None else tuple(self._hole_cards)

    @property
    def is_mucked(self) -> bool:
        """
        :return: True if this poker player has mucked his/her hand, else False
        """
        return self.__is_mucked

    @property
    def actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        from gameframe.poker.rounds import PlayerRound

        if self is self.game.env.actor:
            return cast(PlayerRound, self.game.env._round).actions
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

        FoldAction(self.game, self).act()

    def check_call(self) -> None:
        """Checks or calls.

        :return: None
        """
        from gameframe.poker.actions import CheckCallAction

        CheckCallAction(self.game, self).act()

    def bet_raise(self, amount: int) -> None:
        """Bets or Raises the amount.

        :param amount: the bet/raise amount
        :return: None
        """
        from gameframe.poker.actions import BetRaiseAction

        BetRaiseAction(self.game, self, amount).act()

    def showdown(self, show: bool = False) -> None:
        """Showdowns the hand of this player if necessary or specified.

        :param show: a boolean value on whether or not to show regardless of necessity
        :return: None
        """
        from gameframe.poker.actions import ShowdownAction

        ShowdownAction(self.game, self, show).act()

    def _muck(self) -> None:
        self.__is_mucked = True


A = TypeVar('A', PokerPlayer, PokerNature)


class PokerAction(SeqAction[PokerGame, A], ABC):
    """PokerAction is the abstract base class for all poker actions."""

    def _change_round(self, rnd: Optional[BaseRound] = None) -> None:
        from gameframe.poker.rounds import RoundOpenMixin, RoundCloseMixin

        if isinstance(self.game.env._round, RoundCloseMixin):
            self.game.env._round.close()

        self.game.env._round = rnd if rnd is not None else next(self.game.env._round)

        if isinstance(self.game.env._round, RoundOpenMixin):
            self.game.env._round.open()


class BaseRound(Iterator['BaseRound'], ABC):
    def __init__(self, game: PokerGame):
        self.game = game

    def __next__(self) -> BaseRound:
        from gameframe.poker.rounds import ShowdownRound, DistributionRound

        try:
            return self.game.env._rounds[self.game.env._rounds.index(self) + 1]
        except ValueError:
            if isinstance(self, ShowdownRound):
                return DistributionRound(self.game)
            else:
                return self.game.env._rounds[0]
        except IndexError:
            return ShowdownRound(self.game)
