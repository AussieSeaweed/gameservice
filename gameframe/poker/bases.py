from __future__ import annotations

from abc import ABC, abstractmethod
from itertools import zip_longest
from typing import Any, Iterable, Optional

from gameframe.game import Environment, Nature, Player
from gameframe.poker.utils import Card
from gameframe.poker.utils.decks import Deck
from gameframe.poker.utils.evaluators import Evaluator
from gameframe.sequential import SequentialAction, SequentialGame


class PokerGame(SequentialGame['PokerGame', 'PokerEnvironment', 'PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self: PokerGame) -> None:
        super().__init__()

        if not len(self.starting_stacks) > 1:
            raise ValueError('Poker is played by more than 2 players')

        self._deck: Deck = self._create_deck()
        self._evaluator: Evaluator = self._create_evaluator()

        self._setup()

    @property
    @abstractmethod
    def ante(self: PokerGame) -> int:
        """
        :return: the ante of the poker game
        """
        pass

    @property
    @abstractmethod
    def blinds(self: PokerGame) -> list[int]:
        """
        :return: the blinds of the poker game
        """
        pass

    @property
    @abstractmethod
    def starting_stacks(self: PokerGame) -> list[int]:
        """
        :return: the starting stacks of the poker game
        """
        pass

    def _setup(self: PokerGame) -> None:
        blinds: Iterable[int] = reversed(self.blinds) if len(self.players) == 2 else self.blinds

        for player, starting_stack, blind in zip_longest(self.players, self.starting_stacks, blinds):
            player.stack = starting_stack

            ante: int = min(self.ante, player.stack)

            player.stack -= ante
            self.environment._pot += ante

            if blind is not None:
                blind: int = min(blind, player.stack)

                player.stack -= blind
                player.bet += blind

    def _create_environment(self: PokerGame) -> PokerEnvironment:
        return PokerEnvironment(self)

    def _create_nature(self: PokerGame) -> PokerNature:
        return PokerNature(self)

    def _create_players(self: PokerGame) -> list[PokerPlayer]:
        return [PokerPlayer(self) for _ in range(len(self.starting_stacks))]

    @property
    def _information(self: PokerGame) -> dict[str, Any]:
        return {
            **super()._information,
            'ante': self.ante,
            'blinds': self.blinds,
            'starting_stacks': self.starting_stacks,
        }

    @property
    def _initial_player(self: PokerGame) -> PokerNature:
        return self.nature

    @abstractmethod
    def _create_deck(self: PokerGame) -> Deck:
        pass

    @abstractmethod
    def _create_evaluator(self: PokerGame) -> Evaluator:
        pass


class PokerEnvironment(Environment[PokerGame, 'PokerEnvironment', 'PokerNature', 'PokerPlayer']):
    """PokerEnvironment is the class for poker environments."""

    def __init__(self: PokerEnvironment, game: PokerGame) -> None:
        super().__init__(game)

        self.__board: list[Card] = []
        self._pot: int = 0

        self._aggressor: Optional[PokerPlayer] = None
        self._max_delta: Optional[int] = None

    @property
    def board(self: PokerEnvironment) -> list[Card]:
        """
        :return: the board of the poker environment
        """
        return self.__board

    @property
    def pot(self: PokerEnvironment) -> int:
        """
        :return: the pot of the poker environment
        """
        return self._pot

    @property
    def _information(self: PokerEnvironment) -> dict[str, Any]:
        return {
            **super()._information,
            'pot': self.pot,
            'board': self.board,
        }


class PokerNature(Nature[PokerGame, PokerEnvironment, 'PokerNature', 'PokerPlayer']):
    """PokerNature is the class for poker natures."""

    @property
    def actions(self: PokerNature) -> list[PokerAction]:
        return [
            # TODO: what actions?
        ]

    @property
    def payoff(self: PokerNature) -> int:
        return 0


class PokerPlayer(Player[PokerGame, PokerEnvironment, PokerNature, 'PokerPlayer']):
    """PokerPlayer is the class for poker players."""

    @property
    def actions(self: PokerPlayer) -> list[PokerAction]:
        return [
            # TODO: what actions?
        ]

    @property
    def payoff(self: PokerPlayer) -> int:
        return 0


class PokerAction(SequentialAction[PokerGame, PokerEnvironment, PokerNature, PokerPlayer], ABC):
    """PokerAction is the abstract base class for all poker actions."""

    @property
    def public(self: PokerAction) -> bool:
        return True
