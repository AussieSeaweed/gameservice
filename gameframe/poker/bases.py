from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum, unique
from itertools import zip_longest
from typing import DefaultDict, Iterator, MutableSequence, Optional, Sequence, Set, Union

from gameframe.game import ParamException
from gameframe.game.generics import A, Actor
from gameframe.poker.utils import Card, CardLike, Deck, Evaluator, Hand
from gameframe.sequential.generics import SeqAction, SeqGame


class PokerGame(SeqGame['PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, stages: Sequence[Stage], deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
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

        if len(players) < 2:
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

        if not self._stage.is_skippable:
            self._stage.open()

    @property
    def deck(self) -> Set[Card]:
        """
        :return: the deck of this poker game
        """
        return set(self._deck)

    @property
    def evaluator(self) -> Evaluator:
        """
        :return: the evaluator of this poker game
        """
        return self.__evaluator

    @property
    def ante(self) -> int:
        """
        :return: the ante of this poker game
        """
        return self.__ante

    @property
    def blinds(self) -> Sequence[int]:
        """
        :return: the blinds of this poker game
        """
        return self.__blinds

    @property
    def starting_stacks(self) -> Sequence[int]:
        """
        :return: the starting stacks of this poker game
        """
        return self.__starting_stacks

    @property
    def board_cards(self) -> Sequence[Card]:
        """
        :return: the board cards of this poker game
        """
        return tuple(self._board_cards)

    @property
    def pot(self) -> int:
        """
        :return: the pot of this poker game
        """
        return sum(min(player._commitment, self._requirement) for player in self.players)

    def _trim(self) -> None:
        requirement = sorted(player._commitment for player in self.players)[-2]

        for player in self.players:
            player._commitment = min(player._commitment, requirement)

        self._requirement = requirement


class PokerNature(Actor[PokerGame]):
    """PokerNature is the class for poker natures."""

    def __repr__(self) -> str:
        return 'PokerNature'

    def deal_player(self, player: PokerPlayer, *hole_cards: CardLike) -> None:
        """Deals the hole cards to a player.

        :param player: the player to deal to
        :param hole_cards: the hole cards to be dealt
        :return: None
        """
        from gameframe.poker.actions import HoleCardDealingAction

        HoleCardDealingAction(self.game, self, player, *hole_cards).act()

    def deal_board(self, *cards: CardLike) -> None:
        """Deals the cards to the board.

        :param cards: the cards to be dealt
        :return: None
        """
        from gameframe.poker.actions import BoardCardDealingAction

        BoardCardDealingAction(self.game, self, *cards).act()


class PokerPlayer(Actor[PokerGame], Iterator['PokerPlayer']):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame):
        super().__init__(game)

        self._commitment = 0
        self._hole_cards: MutableSequence[Card] = []
        self._status = self.HoleCardStatus.DEFAULT

    def __next__(self) -> PokerPlayer:
        return self.game.players[(self.index + 1) % len(self.game.players)]

    def __repr__(self) -> str:
        if self.is_mucked:
            return f'PokerPlayer({self.bet}, {self.stack})'
        else:
            return f'PokerPlayer({self.bet}, {self.stack}, [' + ', '.join(map(str, self._hole_cards)) + '])'

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
    def hole_cards(self) -> Optional[Sequence[Card]]:
        """
        :return: the hole cards of this poker player
        """
        return None if self.is_mucked else tuple(self._hole_cards)

    @property
    def hand(self) -> Hand:
        """
        :return: the hand of this poker player
        """
        return self.game.evaluator.hand(self._hole_cards, self.game.board_cards)

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
        return self._status == self.HoleCardStatus.MUCKED

    @property
    def is_shown(self) -> bool:
        """
        :return: True if this poker player has shown his/her hand, else False
        """
        return self._status == self.HoleCardStatus.SHOWN

    @property
    def _effective_stack(self) -> int:
        try:
            return min(sorted(player.starting_stack for player in self.game.players if not player.is_mucked)[-2],
                       self.starting_stack)
        except IndexError:
            return 0

    @property
    def _is_relevant(self) -> bool:
        return not self.is_mucked and self._commitment < self._effective_stack

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

    @unique
    class HoleCardStatus(Enum):
        DEFAULT = 0
        SHOWN = 1
        MUCKED = 2


class Stage(Iterator['Stage'], ABC):
    def __init__(self, game: PokerGame):
        self.game = game

    def __next__(self) -> Stage:
        try:
            return self.game._stages[self.index + 1]
        except IndexError:
            raise StopIteration

    @property
    def target_hole_card_count(self) -> int:
        from gameframe.poker.stages import DealingStage

        count = 0

        for stage in self.game._stages[:self.index + 1]:
            if isinstance(stage, DealingStage):
                count += len(stage.hole_card_statuses)

        return count

    @property
    def target_board_card_count(self) -> int:
        from gameframe.poker.stages import DealingStage

        count = 0

        for stage in self.game._stages[:self.index + 1]:
            if isinstance(stage, DealingStage):
                count += stage.board_card_count

        return count

    @property
    def is_skippable(self) -> bool:
        return sum(not player.is_mucked for player in self.game.players) == 1

    @property
    def index(self) -> int:
        return self.game._stages.index(self)

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


class PokerAction(SeqAction[PokerGame, A], ABC):
    def act(self) -> None:
        super().act()

        if self.game._stage.is_skippable:
            self.game._stage.close()

            try:
                while self.game._stage.is_skippable:
                    self.game._stage = next(self.game._stage)

                self.game._stage.open()
            except StopIteration:
                self.game._trim()
                self.__distribute()
        else:
            self.game._stage.update()

    def __distribute(self) -> None:
        players = list(filter(lambda player: not player.is_mucked, self.game.players))
        revenues: DefaultDict[PokerPlayer, int] = defaultdict(int)

        if len(players) != 1:
            players.sort(key=lambda player: (player.hand, -player._commitment), reverse=True)

        base = 0

        for base_player in players:
            side_pot = self.__side_pot(base, base_player)

            recipients = list(filter(lambda player: player is base_player or player.hand == base_player.hand, players))

            for recipient in recipients:
                revenues[recipient] += side_pot // len(recipients)
            else:
                revenues[recipients[0]] += side_pot % len(recipients)

            base = max(base, base_player._commitment)

        for player, revenue in revenues.items():
            player._commitment -= revenue

        self.game._actor = None

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot = 0

        for player in self.game.players:
            entitlement = min(player._commitment, base_player._commitment)

            if base < entitlement:
                side_pot += entitlement - base

        return side_pot
