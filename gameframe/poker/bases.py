from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Sequence
from enum import Enum, auto
from random import sample
from typing import Final, Optional, Union, cast, final, overload

from auxiliary import default, ilen, iter_equal, retain_iter
from pokertools import Card, Deck, Evaluator, Hand, HoleCard

from gameframe.exceptions import ActionException, ParameterException
from gameframe.poker.exceptions import BetRaiseAmountException, CardCountException, PlayerException
from gameframe.sequential import SequentialGame


@final
class PokerNature:
    """PokerNature is the class for poker natures."""

    def __init__(self, game: Poker):
        self.__game = game

    def __repr__(self) -> str:
        return 'PokerNature'

    @property
    def dealable_players(self) -> Iterator[PokerPlayer]:
        """
        :return: The players that can be dealt.
        """
        return filter(self.can_deal_hole, self.__game.players)

    @property
    def hole_deal_count(self) -> int:
        """
        :return: The number of hole cards to deal to a player.
        """
        from gameframe.poker.parameters import HoleDealingStage

        if self.can_deal_hole():
            return cast(HoleDealingStage, self.__game._stage)._card_count
        else:
            raise ActionException('The poker nature cannot deal hole cards')

    @property
    def board_deal_count(self) -> int:
        """
        :return: The number of cards to deal to the board.
        """
        from gameframe.poker.parameters import BoardDealingStage

        if self.can_deal_board():
            return cast(BoardDealingStage, self.__game._stage)._card_count
        else:
            raise ActionException('The poker nature cannot deal board cards')

    def deal_hole(self, player: PokerPlayer, cards: Optional[Iterable[Card]] = None) -> None:
        """Deals the hole cards to the specified player.

        :param player: The player to deal to.
        :param cards: The hole cards to be dealt.
        :return: None.
        """
        from gameframe.poker._actions import HoleDealingAction

        if cards is None:
            cards = sample(tuple(self.__game._deck), self.hole_deal_count)

        HoleDealingAction(self.__game, self, player, cards).act()

    @overload
    def can_deal_hole(self) -> bool:
        ...

    @overload
    def can_deal_hole(self, player: PokerPlayer) -> bool:
        ...

    @overload
    def can_deal_hole(self, player: PokerPlayer, cards: Iterable[Card]) -> bool:
        ...

    def can_deal_hole(self, player: Optional[PokerPlayer] = None, cards: Optional[Iterable[Card]] = None) -> bool:
        """Determines if the hole cards can be dealt to the specified player.

        :param player: The player to deal to.
        :param cards: The hole cards to be dealt.
        :return: True if the player can be dealt, else False.
        """
        from gameframe.poker._actions import HoleDealingAction

        try:
            HoleDealingAction(self.__game, self, default(player, self.__game.players[0]), default(cards, ())).verify()
        except PlayerException:
            return player is None
        except CardCountException:
            return cards is None
        except ActionException:
            return False
        else:
            return True

    def deal_board(self, cards: Optional[Iterable[Card]] = None) -> None:
        """Deals the cards to the board. Randomly samples cards from the deck if none is given as cards.

        :param cards: The cards to be dealt.
        :return: None.
        """
        from gameframe.poker._actions import BoardDealingAction

        if cards is None:
            cards = sample(tuple(self.__game._deck), self.board_deal_count)

        BoardDealingAction(self.__game, self, cards).act()

    def can_deal_board(self, cards: Optional[Iterable[Card]] = None) -> bool:
        """Determines if the cards can be dealt to the board.

        :param cards: The cards to be dealt.
        :return: True if the board can be dealt, else False.
        """
        from gameframe.poker._actions import BoardDealingAction

        try:
            BoardDealingAction(self.__game, self, default(cards, ())).verify()
        except CardCountException:
            return cards is None
        except ActionException:
            return False
        else:
            return True


@final
class PokerPlayer:
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: Poker, stack: int):
        self.__game = game
        self.starting_stack: Final = stack

        self._stack = stack
        self._bet = 0
        self._hole = list[HoleCard]()
        self._status = self._Status.DEFAULT

    def __repr__(self) -> str:
        if self.mucked:
            return f'PokerPlayer({self._bet}, {self._stack})'
        else:
            return f'PokerPlayer({self._bet}, {self._stack}, ' + ''.join(map(str, self.hole)) + ')'

    @property
    def stack(self) -> int:
        """
        :return: The stack of this poker player.
        """
        return self._stack

    @property
    def bet(self) -> int:
        """
        :return: The bet of this poker player.
        """
        return self._bet

    @property
    def hole(self) -> Sequence[HoleCard]:
        """
        :return: The hole cards of this poker player.
        """
        if self.mucked:
            return tuple(HoleCard(card, False) for card in self._hole)
        elif self.shown:
            return tuple(HoleCard(card, True) for card in self._hole)
        else:
            return tuple(self._hole)

    @property
    def mucked(self) -> bool:
        """
        :return: True if this poker player has mucked his/her hand, else False.
        """
        return self._status == self._Status.MUCKED

    @property
    def shown(self) -> bool:
        """
        :return: True if this poker player has shown his/her hand, else False.
        """
        return self._status == self._Status.SHOWN

    @property
    def hand(self) -> Hand:
        """
        :return: The hand of this poker player.
        """
        return self.__game._evaluator.hand(self._hole, self.__game._board)

    @property
    def min_bet_raise(self) -> int:
        """
        :return: The minimum bet/raise amount.
        """
        if self.can_bet_raise():
            return self.__game._limit._min_amount(self.__game)
        else:
            raise ActionException('The poker player cannot bet/raise')

    @property
    def max_bet_raise(self) -> int:
        """
        :return: The maximum bet/raise amount.
        """
        if self.can_bet_raise():
            return self.__game._limit._max_amount(self.__game)
        else:
            raise ActionException('The poker player cannot bet/raise')

    @property
    def _put(self) -> int:
        return self.starting_stack - self._stack

    @property
    def _total(self) -> int:
        return self._stack + self._bet

    @property
    def _ef_stack(self) -> int:
        try:
            return min(sorted(player.starting_stack for player in self.__game.players if not player.mucked)[-2],
                       self.starting_stack)
        except IndexError:
            return 0

    @property
    def _relevant(self) -> bool:
        return not self.mucked and self._put < self._ef_stack

    def fold(self) -> None:
        """Folds.

        :return: None.
        """
        from gameframe.poker._actions import FoldAction

        FoldAction(self.__game, self).act()

    def can_fold(self) -> bool:
        """Determines if the player can fold.

        :return: True if the player can fold, else False.
        """
        from gameframe.poker._actions import FoldAction

        try:
            FoldAction(self.__game, self).verify()
        except ActionException:
            return False
        else:
            return True

    def check_call(self) -> None:
        """Checks or calls.

        :return: None.
        """
        from gameframe.poker._actions import CheckCallAction

        CheckCallAction(self.__game, self).act()

    def can_check_call(self) -> bool:
        """Determines if the player can check or call.

        :return: True if the player can check or call, else False.
        """
        from gameframe.poker._actions import CheckCallAction

        try:
            CheckCallAction(self.__game, self).verify()
        except ActionException:
            return False
        else:
            return True

    def bet_raise(self, amount: Optional[int] = None) -> None:
        """Bets or Raises the amount.

        :param amount: The bet/raise amount.
        :return: None.
        """
        from gameframe.poker._actions import BetRaiseAction

        BetRaiseAction(self.__game, self, default(amount, self.min_bet_raise)).act()

    def can_bet_raise(self, amount: Optional[int] = None) -> bool:
        """Determines if the player can bet or raise the amount.

        :param amount: The bet/raise amount.
        :return: True if the player can bet or raise the amount, else False.
        """
        from gameframe.poker._actions import BetRaiseAction

        try:
            BetRaiseAction(self.__game, self, default(amount, 0)).verify()
        except BetRaiseAmountException:
            return amount is None
        except ActionException:
            return False
        else:
            return True

    @retain_iter
    def discard_draw(self, discards: Iterable[Card] = (), draws: Optional[Iterable[Card]] = None) -> None:
        """Discards and draws the cards.

        :param discards: The cards to be drawn from the player.
        :param draws: The optional cards to be drawn to the player.
        :return: None.
        """
        from gameframe.poker._actions import DiscardDrawAction

        if draws is None:
            draws = sample(tuple(self.__game._deck), ilen(discards))

        DiscardDrawAction(self.__game, self, discards, draws).act()

    @overload
    def can_discard_draw(self) -> bool:
        ...

    @overload
    def can_discard_draw(self, discards: Iterable[Card]) -> bool:
        ...

    @overload
    def can_discard_draw(self, discards: Iterable[Card], draws: Iterable[Card]) -> bool:
        ...

    def can_discard_draw(self, discards: Iterable[Card] = (), draws: Optional[Iterable[Card]] = None) -> bool:
        """Determines if the player can discard and draw the cards.

        :param discards: The cards to be drawn from the player.
        :param draws: The optional cards to be drawn to the player.
        :return: True if the player can draw, else False.
        """
        from gameframe.poker._actions import DiscardDrawAction

        try:
            DiscardDrawAction(self.__game, self, discards, default(draws, ())).verify()
        except CardCountException:
            return draws is None
        except ActionException:
            return False
        else:
            return True

    def showdown(self, force: bool = False) -> None:
        """Showdowns the hand of this player if necessary or forced.

        :param force: True to force showdown.
        :return: None.
        """
        from gameframe.poker._actions import ShowdownAction

        ShowdownAction(self.__game, self, force).act()

    def can_showdown(self, force: Optional[bool] = None) -> bool:
        """Determines if the player can showdown the his/her hand if necessary or forced.

        :param force: True to force showdown.
        :return: True if the player can showdown, else False.
        """
        from gameframe.poker._actions import ShowdownAction

        try:
            ShowdownAction(self.__game, self, default(force, False)).verify()
        except ActionException:
            return False
        else:
            return True

    class _Status(Enum):
        DEFAULT = auto()
        MUCKED = auto()
        SHOWN = auto()


class Poker(SequentialGame[PokerNature, PokerPlayer]):
    """Poker is the abstract base class for all poker games.

       When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
       invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
       should override the ante, blinds, and starting_stacks properties accordingly.

       The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, stages: Iterable[Stage], limit: Limit, evaluator: Evaluator, deck: Deck,
                 ante: int, blinds: Iterable[int], stacks: Iterable[int]):
        super().__init__(actor := PokerNature(self), (PokerPlayer(self, stack) for stack in stacks), actor)
        from gameframe.poker.parameters import _ShowdownStage

        self.ante: Final = ante
        self.blinds: Final = tuple(blinds)

        self._stages = tuple(stages) + (_ShowdownStage(),)
        self._stage = self._stages[0]

        self._limit = limit
        self._evaluator = evaluator
        self._deck = deck

        self._pot = 0
        self._board = list[Card]()

        self._aggressor = self.players[0] if len(self.players) == 2 else self.players[len(self.blinds) - 1]
        self._max_delta = 0
        self._bet_raise_count = 0

        if len(self.players) < 2:
            raise ParameterException('Poker needs at least 2 players')
        elif not iter_equal(self.blinds, sorted(self.blinds)):
            raise ParameterException('Blinds have to be sorted')
        elif len(self.blinds) > len(self.players):
            raise ParameterException('There are more blinds than players')

        self._tax()

        if not self._stage._skippable(self):
            self._stage._open(self)

    @property
    @final
    def deck(self) -> Iterator[Card]:
        """
        :return: The deck of this poker game.
        """
        return iter(self._deck)

    @property
    @final
    def board(self) -> Sequence[Card]:
        """
        :return: The board cards of this poker game.
        """
        return tuple(self._board)

    @property
    @final
    def pot(self) -> int:
        """
        :return: The pot of this poker game.
        """
        return self._pot

    def _tax(self) -> None:
        for player in self.players:
            cur_ante = min(self.ante, player._stack)

            player._stack -= cur_ante
            self._pot += cur_ante

        for player, blind in zip(self.players, reversed(tuple(self.blinds)) if len(self.players) == 2 else self.blinds):
            blind = min(blind, player._stack)

            player._stack -= blind
            player._bet = blind

    def _reset(self) -> None:
        entitlement = sorted(player._bet for player in self.players)[-2]

        for player in self.players:
            cur_entitlement = min(entitlement, player._bet)

            self._pot += cur_entitlement
            player._stack += player._bet - cur_entitlement
            player._bet = 0


class Stage(ABC):
    """Stage is the abstract base class for all stages."""

    def _skippable(self, game: Poker) -> bool:
        return sum(not player.mucked for player in game.players) == 1

    def _open(self, game: Poker) -> None:
        game._actor = self._opener(game)

    def _close(self, game: Poker) -> None:
        pass

    def _update(self, game: Poker) -> None:
        pass

    @abstractmethod
    def _opener(self, game: Poker) -> Union[PokerNature, PokerPlayer]:
        pass


class Limit(ABC):
    """Limit is the abstract base class for all limits."""

    _max_count: Optional[int]

    @classmethod
    def _min_amount(cls, game: Poker) -> int:
        return min(max(player._bet for player in game.players) + game._max_delta, cast(PokerPlayer, game._actor)._total)

    @abstractmethod
    def _max_amount(self, game: Poker) -> int:
        pass
