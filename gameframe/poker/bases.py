from __future__ import annotations

from abc import ABC
from itertools import zip_longest
from typing import Generic, Iterator, MutableSequence, Optional, Sequence, TypeVar, Union, cast

from gameframe.game import ParamException
from gameframe.game.generics import A, Actor
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

    def __init__(self, stages: Sequence[Stage], deck: Deck, evaluator: Evaluator, ante: int, blinds: Sequence[int],
                 stacks: Sequence[int]):
        nature = PokerNature(self)

        super().__init__(PokerEnv(self, nature, stages, deck, evaluator, ante, blinds), nature,
                         [PokerPlayer(self, stack) for stack in stacks])

        if len(self.players) < 2:
            raise ParamException('Poker needs at least 2 players')
        elif any(a != b for a, b in zip_longest(blinds, sorted(blinds))):
            raise ParamException('Blinds have to be sorted')
        elif len(blinds) > len(self.players):
            raise ParamException('There are more blinds than players')


class PokerEnv(SeqEnv[PokerGame, 'PokerNature', 'PokerPlayer']):
    """PokerEnv is the class for poker environments."""

    def __init__(self, game: PokerGame, actor: PokerNature, stages: Sequence[Stage], deck: Deck, evaluator: Evaluator,
                 ante: int, blinds: Sequence[int]):
        from gameframe.poker.stages import SetupStage

        super().__init__(game, actor)

        self._stage: Stage = SetupStage(game)
        self._stages = stages

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

        SetupAction(self.game, self).act()

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

    def __next__(self) -> PokerPlayer:
        from gameframe.poker.stages import BettingStage, OpenStage

        if isinstance(self.game.env._stage, BettingStage):
            if self is self.game.env._stage.aggressor:
                return self

            player = self.game.players[(self.index + 1) % len(self.game.players)]

            if player._is_relevant:
                return player
            else:
                return next(player)
        elif isinstance(self.game.env._stage, OpenStage):
            if self is self.game.env._stage.opener:
                return self

            player = self.game.players[(self.index + 1) % len(self.game.players)]

            if not player.is_mucked:
                return player
            else:
                return next(player)

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
    def _effective_total(self) -> int:
        return min(sorted(player._total for player in self.game.players if not player.is_mucked)[-2], self._total)

    @property
    def _is_relevant(self) -> bool:
        return not self.is_mucked and self._commitment < self._effective_total

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

        for card in self._hole_cards:
            card._status = False


class Stage(Iterator['Stage'], ABC):
    def __init__(self, game: PokerGame):
        self.game = game

    def __next__(self) -> Stage:
        from gameframe.poker.stages import DistributionStage, MidStage, SetupStage, ShowdownStage

        if isinstance(self, SetupStage):
            stage = self.game.env._stages[0]
        elif isinstance(self, ShowdownStage):
            stage = DistributionStage(self.game)
        elif self is self.game.env._stages[-1]:
            stage = ShowdownStage(self.game)
        else:
            stage = self.game.env._stages[self.index + 1]

        return next(stage) if isinstance(stage, MidStage) and stage.skip else stage

    @property
    def index(self) -> int:
        return self.game.env._stages.index(self)


S = TypeVar('S', bound=Stage)


class PokerAction(SeqAction[PokerGame, A], Generic[A, S], ABC):
    def __init__(self, game: PokerGame, actor: A) -> None:
        super().__init__(game, actor)

        self.stage = cast(S, game.env._stage)

    def change_stage(self) -> None:
        from gameframe.poker.stages import CloseMixin, OpenMixin

        if isinstance(self.game.env._stage, CloseMixin):
            self.game.env._stage.close()

        self.game.env._stage = next(self.game.env._stage)

        if isinstance(self.game.env._stage, OpenMixin):
            self.game.env._stage.open()
