from __future__ import annotations

from abc import ABC
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING, Union, final

from gameframe.game import Actor, Environment
from gameframe.poker.exceptions import InsufficientPlayerCountException, InvalidBlindConfigurationException
from gameframe.sequential import SequentialAction, SequentialGame
from gameframe.utils import override

if TYPE_CHECKING:
    from gameframe.poker import Card, Deck, Evaluator, Hand, HoleCard, Round, Limit


class PokerGame(SequentialGame['PokerGame', 'PokerEnvironment', 'PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self, deck: Deck, evaluator: Evaluator, limit: Limit, rounds: List[Round],
                 ante: int, blinds: Sequence[int], starting_stacks: Sequence[int], lazy: bool) -> None:
        super().__init__(PokerEnvironment(self), PokerNature(self),
                         [PokerPlayer(self) for _ in range(len(starting_stacks))], None)

        self._deck: Deck = deck
        self._evaluator: Evaluator = evaluator
        self._limit: Limit = limit
        self._rounds: List[Optional[Round]] = [None, *rounds]

        self._ante: int = ante
        self._blinds: Sequence[int] = blinds
        self._starting_stacks: Sequence[int] = starting_stacks

        self._lazy: bool = lazy

        if len(self.players) < 2:
            raise InsufficientPlayerCountException()
        elif self._blinds != sorted(self._blinds):
            raise InvalidBlindConfigurationException()

        self._setup()

    @property
    @final
    def ante(self) -> int:
        """
        :return: the ante of the poker game
        """
        return self._ante

    @property
    @final
    def blinds(self) -> Sequence[int]:
        """
        :return: the blinds of the poker game
        """
        return self._blinds

    @property
    @final
    def starting_stacks(self) -> Sequence[int]:
        """
        :return: the starting stacks of the poker game
        """
        return self._starting_stacks

    @property
    @final
    def _round(self) -> Optional[Round]:
        return self._rounds[0] if self._rounds else None

    @property
    @final
    @override
    def _information(self) -> Dict[str, Any]:
        return {
            **super()._information,
            'ante': self.ante,
            'blinds': self.blinds,
            'starting_stacks': self.starting_stacks,
        }

    @final
    def _setup(self) -> None:
        for player, stack in zip(self.players, self._starting_stacks):
            player._stack = stack

        for player in self.players:
            ante: int = min(self._ante, player._stack)

            player._stack -= ante

        for player, blind in zip(self.players, reversed(self._blinds) if len(self.players) == 2 else self._blinds):
            blind: int = min(blind, player.stack)

            player._stack -= blind
            player._bet += blind


@final
class PokerEnvironment(Environment[PokerGame, 'PokerEnvironment', 'PokerNature', 'PokerPlayer']):
    """PokerEnvironment is the class for poker environments."""

    def __init__(self, game: PokerGame) -> None:
        super().__init__(game)

        self._aggressor: Optional[PokerPlayer] = None
        self._max_delta: Optional[int] = None
        self.__board_cards: List[Card] = []

    @property
    def board_cards(self) -> List[Card]:
        """
        :return: the board cards of the poker environment
        """
        return self.__board_cards

    @property
    def pot(self) -> int:
        """
        :return: the pot of the poker environment
        """
        return sum(self.game.starting_stacks) - sum(player._total for player in self.game.players)

    @property
    @override
    def _information(self) -> Dict[str, Any]:
        return {
            **super()._information,
            'pot': self.pot,
            'board_cards': self.board_cards,
        }


@final
class PokerNature(Actor[PokerGame, PokerEnvironment, 'PokerNature', 'PokerPlayer']):
    """PokerNature is the class for poker natures."""

    @property
    @override
    def actions(self) -> Sequence[PokerAction]:
        from gameframe.poker import RoundAction

        return [RoundAction(self)] if self is self.game.actor else []

    @property
    @override
    def payoff(self) -> int:
        return 0


@final
class PokerPlayer(Actor[PokerGame, PokerEnvironment, PokerNature, 'PokerPlayer']):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame) -> None:
        super().__init__(game)

        self._bet: int = 0
        self._stack: int = 0
        self.__hole_cards: Optional[List[HoleCard]] = []

    @property
    def bet(self) -> int:
        """
        :return: the bet of the poker player
        """
        return self._bet

    @property
    def hole_cards(self) -> Optional[List[HoleCard]]:
        """
        :return: the hole cards of the poker player
        """
        return self.__hole_cards

    @property
    def stack(self) -> int:
        """
        :return: the stack of the poker player
        """
        return self._stack

    @property
    @override
    def actions(self) -> Sequence[PokerAction]:
        return self.game._round._create_actions() if self is self.game.actor and self.game._round is not None else []

    @property
    @override
    def payoff(self) -> int:
        return -self._commitment

    @override
    def __next__(self) -> Union[PokerNature, PokerPlayer]:
        player: Union[PokerNature, PokerPlayer] = super().__next__()

        while not player._relevant and player is not self.game.environment._aggressor and player is not self:
            player: Union[PokerNature, PokerPlayer] = Actor.__next__(player)

        return self.game.nature if player is self.game.environment._aggressor or player is self else player

    @property
    def _commitment(self) -> int:
        return self._starting_stack - self.stack

    @property
    def _effective_stack(self) -> int:
        try:
            return min(sorted(player._total for player in self.game.players if not player._mucked)[-2], self._total)
        except IndexError:
            return 0

    @property
    def _hand(self) -> Hand:
        return self.game._evaluator.hand(self.hole_cards, self.game.environment.board_cards)

    @property
    def _mucked(self) -> bool:
        return self.hole_cards is None

    @property
    def _relevant(self) -> bool:
        return not self._mucked and self.stack > 0 and self._effective_stack > 0

    @property
    def _starting_stack(self) -> int:
        return self.game._starting_stacks[self.index]

    @property
    def _total(self) -> int:
        return self.bet + self.stack

    @property
    @override
    def _private_information(self) -> Dict[str, Any]:
        return {
            **super()._private_information,
            'hole_cards': self.hole_cards,
        }

    @property
    @override
    def _public_information(self) -> Dict[str, Any]:
        return {
            **super()._public_information,
            'bet': self.bet,
            'stack': self.stack,
            'hole_cards': None if self.hole_cards is None else list(map(
                lambda hole_card: hole_card if hole_card.status else None,
                self.hole_cards,
            )),
        }

    def _muck(self) -> None:
        self.__hole_cards: Optional[List[HoleCard]] = None


class PokerAction(SequentialAction[PokerGame, PokerEnvironment, PokerNature, PokerPlayer], ABC):
    """PokerAction is the abstract base class for all poker actions."""

    def __init__(self, actor: Union[PokerNature, PokerPlayer], chance: bool) -> None:
        super().__init__(actor, chance, True)


class PokerPlayerAction(PokerAction, ABC):
    """PokerPlayerAction is the abstract base class for all poker player actions."""

    def __init__(self, actor: PokerPlayer) -> None:
        super().__init__(actor, False)


class PokerNatureAction(PokerAction, ABC):
    """PokerNatureAction is the abstract base class for all poker nature actions."""

    def __init__(self, actor: PokerNature) -> None:
        super().__init__(actor, True)
