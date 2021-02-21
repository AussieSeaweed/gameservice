from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Iterator, MutableSequence, Sequence, defaultdict
from enum import Enum, unique
from functools import cached_property
from itertools import zip_longest
from typing import Optional, Union, cast, final

from pokertools import Card, Deck, Evaluator, Hand, HoleCard

from gameframe.game import ActionException, ParamException
from gameframe.game._generics import A, Actor
from gameframe.poker.exceptions import BetRaiseAmountException, CardCountException, InvalidPlayerException
from gameframe.sequential._generics import SeqAction, SeqGame


class PokerGame(SeqGame['PokerNature', 'PokerPlayer', Union['PokerNature', 'PokerPlayer']], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, stages: Sequence[_Stage], deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 starting_stacks: Sequence[int]):
        nature = PokerNature(self)
        players = [PokerPlayer(self) for _ in starting_stacks]
        actor = nature

        super().__init__(nature, players, actor)

        self._stages = stages
        self._stage = stages[0]

        self._deck = deck
        self.__evaluator = evaluator
        self.__ante = ante
        self.__blinds = tuple(blinds)
        self.__starting_stacks = tuple(starting_stacks)

        self._board_cards: MutableSequence[Card] = []
        self._aggressor = players[0] if len(players) == 2 else players[blinds.index(max(blinds))]
        self._max_delta = 0
        self._requirement = ante

        if not isinstance(ante, int) or not all(isinstance(blind, int) for blind in blinds) \
                or not all(isinstance(stack, int) for stack in starting_stacks):
            raise TypeError('The integral values must be of type int')
        elif len(players) < 2:
            raise ParamException('Poker needs at least 2 players')
        elif any(a != b for a, b in zip_longest(blinds, sorted(blinds))):
            raise ParamException('Blinds have to be sorted')
        elif len(blinds) > len(players):
            raise ParamException('There are more blinds than players')
        elif len(blinds) != len(set(blinds)):
            raise ParamException('Each blind value must be unique')

        if len(players) == 2:
            blinds = list(reversed(blinds))

        for player, blind, starting_stack in zip_longest(players, blinds, starting_stacks, fillvalue=0):
            player._commitment = min(ante + blind, starting_stack)

        if not self._stage.skippable:
            self._stage.open()

    @property
    @final
    def deck(self) -> Sequence[Card]:
        """
        :return: the deck of this poker game
        """
        return tuple(self._deck)

    @property
    @final
    def evaluator(self) -> Evaluator:
        """
        :return: the evaluator of this poker game
        """
        return self.__evaluator

    @property
    @final
    def ante(self) -> int:
        """
        :return: the ante of this poker game
        """
        return self.__ante

    @property
    @final
    def blinds(self) -> Sequence[int]:
        """
        :return: the blinds of this poker game
        """
        return self.__blinds

    @property
    @final
    def starting_stacks(self) -> Sequence[int]:
        """
        :return: the starting stacks of this poker game
        """
        return self.__starting_stacks

    @property
    @final
    def board_cards(self) -> Sequence[Card]:
        """
        :return: the board cards of this poker game
        """
        return tuple(self._board_cards)

    @property
    @final
    def pot(self) -> int:
        """
        :return: the pot of this poker game
        """
        return sum(min(player._commitment, self._requirement) for player in self.players)

    @cached_property
    def _hole_card_statuses(self) -> Sequence[bool]:
        from gameframe.poker._stages import HoleCardDealingStage

        statuses: list[bool] = []

        for stage in self._stages:
            if isinstance(stage, HoleCardDealingStage):
                statuses.extend(stage.card_status for _ in range(stage.card_count))

        return statuses

    def _trim(self) -> None:
        requirement = sorted(player._commitment for player in self.players)[-2]

        for player in self.players:
            player._commitment = min(player._commitment, requirement)

        self._requirement = requirement


@final
class PokerNature(Actor[PokerGame]):
    """PokerNature is the class for poker natures."""

    def __repr__(self) -> str:
        return 'PokerNature'

    @property
    def player_deal_count(self) -> int:
        """
        :return: the number of hole cards to deal to a player
        """
        from gameframe.poker._stages import HoleCardDealingStage

        if self.can_deal_player():
            return cast(HoleCardDealingStage, self.game._stage).card_count
        else:
            raise ActionException('The poker nature cannot deal hole cards')

    @property
    def board_deal_count(self) -> int:
        """
        :return: the number of cards to deal to the board
        """
        from gameframe.poker._stages import BoardCardDealingStage

        if self.can_deal_board():
            return cast(BoardCardDealingStage, self.game._stage).card_count
        else:
            raise ActionException('The poker nature cannot deal board cards')

    def deal_player(self, player: PokerPlayer, *cards: Card) -> None:
        """Deals the hole cards to the specified player.

        :param player: the player to deal to
        :param cards: the hole cards to be dealt
        :return: None
        """
        from gameframe.poker._actions import HoleCardDealingAction

        HoleCardDealingAction(self.game, self, player, *cards).act()

    def deal_board(self, *cards: Card) -> None:
        """Deals the cards to the board.

        :param cards: the cards to be dealt
        :return: None
        """
        from gameframe.poker._actions import BoardCardDealingAction

        BoardCardDealingAction(self.game, self, *cards).act()

    def can_deal_player(self, player: Optional[PokerPlayer] = None, *cards: Card) -> bool:
        """Determines if the hole cards can be dealt to the specified player.

        :param player: the player to deal to
        :param cards: the hole cards to be dealt
        :return: True if the player can be dealt, else False
        """
        from gameframe.poker._actions import HoleCardDealingAction

        try:
            HoleCardDealingAction(self.game, self, self.game.players[0] if player is None else player, *cards).verify()
        except InvalidPlayerException:
            return player is None
        except CardCountException:
            return not cards
        except ActionException:
            return False
        else:
            return True

    def can_deal_board(self, *cards: Card) -> bool:
        """Determines if the cards can be dealt to the board.

        :param cards: the cards to be dealt
        :return: True if the board can be dealt, else False
        """
        from gameframe.poker._actions import BoardCardDealingAction

        try:
            BoardCardDealingAction(self.game, self, *cards).verify()
        except CardCountException:
            return not cards
        except ActionException:
            return False
        else:
            return True


@final
class PokerPlayer(Actor[PokerGame], Iterator['PokerPlayer']):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame):
        super().__init__(game)

        self._commitment = 0
        self._hole_cards: MutableSequence[Card] = []
        self._status = _HoleCardStatus.DEFAULT

    def __next__(self) -> PokerPlayer:
        return self.game.players[(self.index + 1) % len(self.game.players)]

    def __repr__(self) -> str:
        if self.mucked:
            return f'PokerPlayer({self.bet}, {self.stack})'
        else:
            return f'PokerPlayer({self.bet}, {self.stack}, [' + ', '.join(map(str, self.hole_cards)) + '])'

    @cached_property
    def index(self) -> int:
        """
        :return: the index of this poker player
        """
        return self.game.players.index(self)

    @property
    def starting_stack(self) -> int:
        """
        :return: the starting stack of this poker player
        """
        return self.game.starting_stacks[self.index]

    @property
    def bet(self) -> int:
        """
        :return: the bet of this poker player
        """
        return max(self._commitment - self.game._requirement, 0)

    @property
    def stack(self) -> int:
        """
        :return: the stack of this poker player
        """
        return self.starting_stack - self._commitment

    @property
    def hole_cards(self) -> Sequence[HoleCard]:
        """
        :return: the hole cards of this poker player
        """
        if self.mucked:
            return tuple(HoleCard(card, False) for card in self._hole_cards)
        elif self.shown:
            return tuple(HoleCard(card, True) for card in self._hole_cards)
        else:
            return tuple(HoleCard(card, status) for card, status in
                         zip(self._hole_cards, self.game._hole_card_statuses))

    @property
    def hand(self) -> Hand:
        """
        :return: the hand of this poker player
        """
        return self.game.evaluator.hand(self._hole_cards, self.game.board_cards)

    @property
    def mucked(self) -> bool:
        """
        :return: True if this poker player has mucked his/her hand, else False
        """
        return self._status == _HoleCardStatus.MUCKED

    @property
    def shown(self) -> bool:
        """
        :return: True if this poker player has shown his/her hand, else False
        """
        return self._status == _HoleCardStatus.SHOWN

    @property
    def min_bet_raise_amount(self) -> int:
        """
        :return: the minimum bet/raise amount
        """
        from gameframe.poker._stages import BettingStage

        if self.can_bet_raise():
            return cast(BettingStage, self.game._stage).min_amount
        else:
            raise ActionException('The poker player cannot bet/raise')

    @property
    def max_bet_raise_amount(self) -> int:
        """
        :return: the maximum bet/raise amount
        """
        from gameframe.poker._stages import BettingStage

        if self.can_bet_raise():
            return cast(BettingStage, self.game._stage).max_amount
        else:
            raise ActionException('The poker player cannot bet/raise')

    @property
    def _effective_stack(self) -> int:
        try:
            return min(sorted(player.starting_stack for player in self.game.players if not player.mucked)[-2],
                       self.starting_stack)
        except IndexError:
            return 0

    @property
    def _relevant(self) -> bool:
        return not self.mucked and self._commitment < self._effective_stack

    def fold(self) -> None:
        """Folds.

        :return: None
        """
        from gameframe.poker._actions import FoldAction

        FoldAction(self.game, self).act()

    def check_call(self) -> None:
        """Checks or calls.

        :return: None
        """
        from gameframe.poker._actions import CheckCallAction

        CheckCallAction(self.game, self).act()

    def bet_raise(self, amount: int) -> None:
        """Bets or Raises the amount.

        :param amount: the bet/raise amount
        :return: None
        """
        from gameframe.poker._actions import BetRaiseAction

        BetRaiseAction(self.game, self, amount).act()

    def showdown(self, force: bool = False) -> None:
        """Showdowns the hand of this player if necessary or forced.

        :return: None
        """
        from gameframe.poker._actions import ShowdownAction

        ShowdownAction(self.game, self, force).act()

    def can_fold(self) -> bool:
        """Determines if the player can fold.

        :return: True if the player can fold, else False
        """
        from gameframe.poker._actions import FoldAction

        try:
            FoldAction(self.game, self).verify()
        except ActionException:
            return False
        else:
            return True

    def can_check_call(self) -> bool:
        """Determines if the player can check or call.

        :return: True if the player can check or call, else False
        """
        from gameframe.poker._actions import CheckCallAction

        try:
            CheckCallAction(self.game, self).verify()
        except ActionException:
            return False
        else:
            return True

    def can_bet_raise(self, amount: Optional[int] = None) -> bool:
        """Determines if the player can bet or raise the amount.

        :param amount: the bet/raise amount
        :return: True if the player can bet or raise the amount, else False
        """
        from gameframe.poker._actions import BetRaiseAction

        try:
            BetRaiseAction(self.game, self, 0 if amount is None else amount).verify()
        except BetRaiseAmountException:
            return amount is None
        except ActionException:
            return False
        else:
            return True

    def can_showdown(self) -> bool:
        """Determines if the player can showdown the his/her hand if necessary or forced.

        :return: True if the player can showdown, else False
        """
        from gameframe.poker._actions import ShowdownAction

        try:
            ShowdownAction(self.game, self, False).verify()
        except ActionException:
            return False
        else:
            return True


class _Stage(Iterator['_Stage'], ABC):
    def __init__(self, game: PokerGame):
        self.game = game

    def __next__(self) -> _Stage:
        try:
            return self.game._stages[self.index + 1]
        except IndexError:
            raise StopIteration

    @cached_property
    def index(self) -> int:
        return self.game._stages.index(self)

    @property
    def skippable(self) -> bool:
        return sum(not player.mucked for player in self.game.players) == 1

    @property
    @abstractmethod
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        pass

    def open(self) -> None:
        self.game._actor = self.opener

    def close(self) -> None:
        pass

    def update(self) -> None:
        pass


class _PokerAction(SeqAction[PokerGame, A], ABC):
    def act(self) -> None:
        super().act()

        if self.game._stage.skippable:
            self.game._stage.close()

            try:
                while self.game._stage.skippable:
                    self.game._stage = next(self.game._stage)

                self.game._stage.open()
            except StopIteration:
                self.game._trim()
                self.__distribute()
        else:
            self.game._stage.update()

    def __distribute(self) -> None:
        players = list(filter(lambda player: not player.mucked, self.game.players))
        revenues: defaultdict[PokerPlayer, int] = defaultdict(int)

        if len(players) != 1:
            players.sort(key=lambda player: (player.hand, -player._commitment), reverse=True)

        base = 0

        for base_player in players:
            side_pot = self.__get_side_pot(base, base_player)

            recipients = list(filter(lambda player: player is base_player or player.hand == base_player.hand, players))

            for recipient in recipients:
                revenues[recipient] += side_pot // len(recipients)
            else:
                revenues[recipients[0]] += side_pot % len(recipients)

            base = max(base, base_player._commitment)

        for winner, revenue in revenues.items():
            winner._commitment -= revenue

        self.game._actor = None

    def __get_side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot = 0

        for player in self.game.players:
            if base < (entitlement := min(player._commitment, base_player._commitment)):
                side_pot += entitlement - base

        return side_pot


@unique
class _HoleCardStatus(Enum):
    DEFAULT = 0
    SHOWN = 1
    MUCKED = 2
