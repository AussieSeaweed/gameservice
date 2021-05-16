from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Sequence, Set
from enum import Enum, auto
from typing import Final, Optional, final, overload

from auxiliary import after, iter_equal
from pokertools import Card, Deck, Evaluator, Hand, HoleCard

from gameframe.exceptions import GameFrameValueError
from gameframe.sequential import SequentialActor, SequentialGame


class Stage(ABC):
    """Stage is the abstract class for all stages in poker games."""

    @abstractmethod
    def _open(self, game: Poker) -> None: ...

    @abstractmethod
    def _close(self, game: Poker) -> None: ...

    @abstractmethod
    def _done(self, game: Poker) -> bool: ...


class Limit(ABC):
    """Limit is the abstract class for all limits in poker games."""

    _max_bet_raise_count: int

    @abstractmethod
    def _min_amount(self, player: PokerPlayer) -> None: ...

    @abstractmethod
    def _max_amount(self, player: PokerPlayer) -> None: ...


class SidePot:
    """SidePot is the class for side pots."""

    def __init__(self, players: Iterable[PokerPlayer], amount: int):
        self.players: Final = set(players)
        self.amount: Final = amount


class Settings(ABC):
    """Settings is the abstract class for all poker settings."""

    @property
    @abstractmethod
    def ante(self) -> int:
        """Returns the ante of this poker settings.

        :return: The nate of this poker settings.
        """
        ...

    @property
    @abstractmethod
    def blinds(self) -> Sequence[int]:
        """Returns the blinds of this poker settings.

        :return: The blinds of this poker settings.
        """
        ...

    @property
    @abstractmethod
    def starting_stacks(self) -> Sequence[int]:
        """Returns the starting stacks of this poker settings.

        :return: The starting stacks of this poker settings.
        """
        ...

    @property
    @abstractmethod
    def stages(self) -> Sequence[Stage]:
        """Returns the stages of this poker settings.

        :return: The stages of this poker settings.
        """
        ...

    @property
    @abstractmethod
    def limit(self) -> Limit:
        """Returns the limit of this poker settings.

        :return: The limit of this poker settings.
        """
        ...

    @property
    @abstractmethod
    def evaluators(self) -> Sequence[Evaluator]:
        """Returns the evaluator of this poker settings.

        :return: The evaluator of this poker settings.
        """
        ...

    @property
    @abstractmethod
    def deck(self) -> Deck:
        """Returns the deck of this poker settings.

        :return: The deck of this poker settings.
        """
        ...


class Poker(SequentialGame['Poker', 'PokerNature', 'PokerPlayer'], ABC):
    """Poker is the abstract class for all poker games."""

    def __init__(self, settings: Settings):
        self.ante: Final = settings.ante
        self.blinds: Final = tuple(settings.blinds)
        self.starting_stacks: Final = tuple(settings.starting_stacks)
        self.stages: Final = tuple(settings.stages)
        self.limit: Final = settings.limit
        self.evaluators: Final = tuple(settings.evaluators)

        if len(self.starting_stacks) < 2:
            raise GameFrameValueError('Poker needs at least 2 players')
        elif not iter_equal(self.blinds, sorted(self.blinds)):
            raise GameFrameValueError('Blinds must be sorted')
        elif len(self.blinds) > len(self.starting_stacks):
            raise GameFrameValueError('Number of blinds must be less than or equal to the number of players')
        elif not self.stages:
            raise GameFrameValueError('Number of stages must be at least 1')

        self._deck = settings.deck
        self._stage = self.stages[0]

        self._pot = 0
        self._board = list[Card]()
        self._player_queue = list[PokerPlayer]()

        self._nature = PokerNature(self)
        self._players = [PokerPlayer(self) for _ in range(len(self.starting_stacks))]
        self._actor = None

        self._setup()

    @property
    def deck(self) -> Set[Card]:
        """Returns the deck of this poker game.

        :return: The deck of this poker game.
        """
        return self._deck

    @property
    def stage(self) -> Stage:
        """Returns the stage of this poker game.

        :return: The stage of this poker game.
        """
        return self._stage

    @property
    def pot(self) -> int:
        """Returns the pot of this poker game.

        :return: The pot of this poker game.
        """
        return self._pot

    @property
    def board(self) -> Sequence[Card]:
        """Returns the board of this poker game.

           The board contains the public cards in a poker game. They can be combined with individual player's hole cards
           to create a hand.

        :return: The board of this poker game.
        """
        return self._board

    @property
    def side_pots(self) -> Sequence[SidePot]:
        """Returns the side pots of this poker game.

        :return: The side pots of this poker game.
        """
        players = sorted(self.players, key=lambda player: player.starting_stack)
        side_pots = list[SidePot]()
        pot = 0
        prev = 0

        while pot < self.pot:
            cur = min(-player.payoff for player in players)
            amount = len(players) * (cur - prev)

            players = players[1:]
            side_pots.append(SidePot((player for player in players if player.active), amount))
            pot += amount
            prev = cur

        return side_pots

    def _setup(self) -> None:
        for i, (stack, player) in enumerate(zip(self.starting_stacks, self._players)):
            ante = max(self.ante, stack)
            blind = max(0 if i not in self.blinds else self.blinds[i], stack - ante)

            self._pot += ante
            player._bet += blind
            player._stack -= ante + blind

        self.stage._open(self)

    def _collect(self) -> None:
        effective_bet = sorted(player.bet for player in self.players)[-2]

        for player in self.players:
            bet = min(effective_bet, player.bet)
            self._pot += bet
            player._stack += player.bet - bet
            player._bet = 0

    def _update(self) -> None:
        if self.stage._done(self):
            self.stage._close(self)

            try:
                stage = after(self.stages, self.stage)

                while stage._done(self):
                    stage = after(self.stages, stage)
                else:
                    stage._open(self)
                    self._stage = stage
            except ValueError:
                self._distribute()
                self._actor = None

    def _distribute(self) -> None:
        self._collect()

        for side_pot in self.side_pots:
            amounts = [side_pot.amount // len(self.evaluators)] * len(self.evaluators)
            amounts[0] += side_pot.amount % len(self.evaluators)

            for amount, evaluator in zip(amounts, self.evaluators):
                hand = max(player._hand(evaluator) for player in side_pot.players)
                players = [player for player in side_pot.players if player._hand(evaluator) == hand]

                rewards = [amount // len(players)] * len(players)
                rewards[0] += amount % len(players)

                for player, reward in zip(players, rewards):
                    player._stack += reward

        self._pot = 0


@final
class PokerNature(SequentialActor[Poker, 'PokerNature', 'PokerPlayer']):
    """PokerNature is the class for poker natures."""

    def __init__(self, game: Poker):
        self._game = game

    @property
    def dealable_players(self) -> Iterator[PokerPlayer]:
        """Returns an iterator of poker players that can be dealt.

        :return: The players that can be dealt.
        """
        ...

    @property
    def hole_deal_count(self) -> int:
        """Returns the number of hole cards that can be dealt.

        :return: The number of hole cards to deal to a player.
        """
        ...

    @property
    def board_deal_count(self) -> int:
        """Returns the number of board cards that can be dealt.

        :return: The number of cards to deal to the board.
        """
        ...

    @overload
    def deal_hole(self) -> None: ...

    @overload
    def deal_hole(self, player: PokerPlayer) -> None: ...

    @overload
    def deal_hole(self, player: PokerPlayer, cards: Iterable[Card]) -> None: ...

    def deal_hole(self, player: Optional[PokerPlayer] = None, cards: Optional[Iterable[Card]] = None) -> None:
        """Deals the optionally supplied hole cards to the optionally specified player.

           If the cards are not supplied, they are randomly drawn from the deck. If the player is not known, the next
           player in order who is dealable will be dealt.

        :param player: The optional player to deal to.
        :param cards: The optional hole cards to be dealt.
        :return: None.
        """
        ...

    @overload
    def can_deal_hole(self) -> bool: ...

    @overload
    def can_deal_hole(self, player: PokerPlayer) -> bool: ...

    @overload
    def can_deal_hole(self, player: PokerPlayer, cards: Iterable[Card]) -> bool: ...

    def can_deal_hole(self, player: Optional[PokerPlayer] = None, cards: Optional[Iterable[Card]] = None) -> bool:
        """Determines if the optionally specified hole cards can be dealt to the opionally supplied player.

        :param player: The optional player to deal to.
        :param cards: The optional hole cards to be dealt.
        :return: True if the hole cards dealt, else False.
        """
        ...

    def deal_board(self, cards: Optional[Iterable[Card]] = None) -> None:
        """Deals the optionally specified cards to the board.

           If none is given as cards, sample cards are randomly selected from the deck.

        :param cards: The optional cards to be dealt.
        :return: None.
        """
        ...

    def can_deal_board(self, cards: Optional[Iterable[Card]] = None) -> bool:
        """Determines if cards can be dealt to the board.

        :param cards: The optional cards to be dealt.
        :return: True if the board can be dealt, else False.
        """
        ...


@final
class PokerPlayer(SequentialActor[Poker, PokerNature, 'PokerPlayer']):
    def __init__(self, game: Poker):
        self._bet = 0
        self._stack = 0
        self._hole = list[HoleCard]()
        self._status: Optional[PokerPlayer._Status] = None
        self._game = game

    @property
    def bet(self) -> int:
        """Returns the bet of this poker player.

        :return: The bet of this poker player.
        """
        return self._bet

    @property
    def stack(self) -> int:
        """Returns the stack of this poker player.

        :return: The stack of this poker player.
        """
        return self._stack

    @property
    def hole(self) -> Sequence[HoleCard]:
        """Returns the hole cards of this poker player.

        :return: The hole cards of this poker player.
        """
        return self._hole

    @property
    def starting_stack(self) -> int:
        """Returns the starting stack of this poker player.

        :return: The starting stack of this poker player.
        """
        return self.game.starting_stacks[self.game.players.index(self)]

    @property
    def total(self) -> int:
        """Returns the total of the bet and the stack of this poker player.

           In other words, returns the sum of this player's bet and stack.

        :return: The total of he bet and the stack of this poker player.
        """
        return self._bet + self._stack

    @property
    def effective_stack(self) -> int:
        """Returns the effective stack of this poker player.

           The effective stacks are maximum amount that the poker player can lose in a current poker game state.

        :return: The effective stack of this poker player.
        """
        active_players = [player for player in self.game.players if player.active]

        if self.mucked or len(active_players) < 2:
            return 0
        else:
            return min(self.total, sorted(player.total for player in active_players)[-2])

    @property
    def payoff(self) -> int:
        """Returns the payoff of this poker player.

           If the player made money, the payoff will be a positive quantity, and vice versa.

        :return: The payoff of this poker player.
        """
        return self.starting_stack - self.total

    @property
    def hands(self) -> Iterator[Hand]:
        """Returns the hands of this poker player.

          The hands are arranged in the order of evaluators of the associated poker game. Usually, poker games only have
          one evaluator type, in which case this property will be a singleton iterator. However, sometimes, a poker game
          may have hi and lo evaluator. Then, this property will be a pair of hi and lo hands.

        :return: The hands of this poker player.
        """
        return (self._hand(evaluator) for evaluator in self.game.evaluators)

    @property
    def mucked(self) -> bool:
        """Returns whether or not the player has mucked his/her hand or not.

        :return: The mucked status of this poker player.
        """
        return self._status == self._Status.MUCKED

    @property
    def shown(self) -> bool:
        """Returns whether or not the player has shown his/her hand or not.

        :return: The shown status of this poker player.
        """
        return self._status == self._Status.SHOWN

    @property
    def active(self) -> bool:
        """Returns whether or not the player is active or not.

           The player is active if he/she is in a hand.

        :return: The active status of this poker player.
        """
        return not self.mucked

    @property
    def min_bet_raise_amount(self) -> int:
        """Returns the minimum bet/raise amount.

        :return: The minimum bet/raise amount.
        """
        ...

    @property
    def max_bet_raise_amount(self) -> int:
        """Returns the maximum bet/raise amount.

        :return: The maximum bet/raise amount.
        """
        ...

    def fold(self) -> None:
        """Folds the poker player's hand.

        :return: None
        """
        ...

    def can_fold(self) -> bool:
        """Returns whether or not the player can fold his/her hand or not.

        :return: True if this poker player can fold, else False
        """
        ...

    def check_call(self) -> None:
        """Checks or calls the opponent's bet.

        :return: None
        """
        ...

    def can_check_call(self) -> bool:
        """Returns whether or not the player can check/call or not.

        :return: True if this poker player can check/call, else False
        """
        ...

    @overload
    def bet_raise(self) -> None:
        ...

    @overload
    def bet_raise(self, amount: int) -> None:
        ...

    def bet_raise(self, amount: Optional[int] = None) -> None:
        """Bets or raises to the optional amount.

           If no amount is specified, this poker player will min-raise.

        :param amount: The optional amount to bet/raise.
        :return: None
        """
        ...

    @overload
    def can_bet_raise(self) -> bool:
        ...

    @overload
    def can_bet_raise(self, amount: int) -> bool:
        ...

    def can_bet_raise(self, amount: Optional[int] = None) -> bool:
        """Returns whether or not the player can bet/raise or not to the optionally given bet amount.

        :param amount: The optional amount to bet/raise.
        :return: True if this poker player can bet/raise, else False
        """
        ...

    @overload
    def discard_draw(self) -> None:
        ...

    @overload
    def discard_draw(self, discarded_cards: Iterable[Card]) -> None:
        ...

    @overload
    def discard_draw(self, discarded_cards: Iterable[Card], drawn_cards: Iterable[Card]) -> None:
        ...

    def discard_draw(
            self,
            discarded_cards: Optional[Iterable[Card]] = None,
            drawn_cards: Optional[Iterable[Card]] = None,
    ) -> None:
        """Discards this poker player's optionally specified hole cards and draws the corresponding optionally given
           cards.

           If the drawn cards are not specified, they are random cards are drawn. If discarded cards are none, the poker
           player performs a stand pat.

        :param discarded_cards: The optional cards to discard.
        :param drawn_cards: The optional cards to draw.
        :return: None
        """
        ...

    @overload
    def can_discard_draw(self) -> bool:
        ...

    @overload
    def can_discard_draw(self, discarded_cards: Iterable[Card]) -> bool:
        ...

    @overload
    def can_discard_draw(self, discarded_cards: Iterable[Card], drawn_cards: Iterable[Card]) -> bool:
        ...

    def can_discard_draw(
            self,
            discarded_cards: Optional[Iterable[Card]] = None,
            drawn_cards: Optional[Iterable[Card]] = None,
    ) -> bool:
        """Returns whether or not this poker player can discard and draw.

        :param discarded_cards: The optional cards to discard.
        :param drawn_cards: The optional cards to draw.
        :return: True if this poker player can discard and draw, else False.
        """
        ...

    def showdown(self, force: bool = False) -> None:
        """Showdowns this poker player's hand if necessary to win the pot or forced.

        :param force: True to force showdown, else False. Defaults to False.
        :return: None
        """
        ...

    def can_showdown(self, force: bool = False) -> bool:
        """Returns whether or not this poker player can showdown.

        :param force: True to force showdown, else False. Defaults to False.
        :return: True if this poker player can showdown, else False.
        """
        ...

    def _hand(self, evaluator: Evaluator) -> Hand:
        return evaluator.hand(self.hole, self.game.board)

    class _Status(Enum):
        MUCKED = auto()
        SHOWN = auto()
