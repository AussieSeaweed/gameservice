from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional, TYPE_CHECKING, Union

from gameframe.game import Environment, Nature, Player
from gameframe.sequential import SequentialAction, SequentialGame

if TYPE_CHECKING:
    from . import Card, Deck, Evaluator, Hand, HoleCard, Round


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
        self._rounds: list[Round] = self._create_rounds()

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
        for player in self.players:
            ante: int = min(self.ante, player.stack)

            player._stack -= ante
            self.environment._pot += ante

        for player, blind in zip(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds):
            blind: int = min(blind, player.stack)

            player._stack -= blind
            player._bet += blind

    def _create_environment(self: PokerGame) -> PokerEnvironment:
        return PokerEnvironment(self)

    def _create_nature(self: PokerGame) -> PokerNature:
        return PokerNature(self)

    def _create_players(self: PokerGame) -> list[PokerPlayer]:
        return [PokerPlayer(self, starting_stack) for starting_stack in self.starting_stacks]

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

    @property
    def _round(self: PokerGame) -> Round:
        return self._rounds[0] if self._rounds else None

    @abstractmethod
    def _create_deck(self: PokerGame) -> Deck:
        pass

    @abstractmethod
    def _create_evaluator(self: PokerGame) -> Evaluator:
        pass

    @abstractmethod
    def _create_rounds(self: PokerGame) -> list[Round]:
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
        return self.game._round._create_actions()

    @property
    def payoff(self: PokerNature) -> int:
        return 0


class PokerPlayer(Player[PokerGame, PokerEnvironment, PokerNature, 'PokerPlayer']):
    """PokerPlayer is the class for poker players."""

    def __init__(self: PokerPlayer, game: PokerGame, starting_stack: int) -> None:
        super().__init__(game)

        self._bet: int = 0
        self._stack: int = 0
        self._hole_cards: Optional[list[HoleCard]] = []

        self.__starting_stack: int = starting_stack

    @property
    def bet(self: PokerPlayer) -> int:
        """
        :return: the bet of the poker player
        """
        return self._bet

    @property
    def stack(self: PokerPlayer) -> int:
        """
        :return: the stack of the poker player
        """
        return self._stack

    @property
    def hole_cards(self: PokerPlayer) -> Optional[list[HoleCard]]:
        """
        :return: the hole cards of the poker player
        """
        return self._hole_cards

    @property
    def mucked(self: PokerPlayer) -> bool:
        """
        :return: True if the poker player has mucked, False otherwise
        """
        return self.hole_cards is None

    @property
    def commitment(self: PokerPlayer) -> int:
        """
        :return: the amount the poker player has put
        """
        return self.__starting_stack - self.stack

    @property
    def total(self: PokerPlayer) -> int:
        """
        :return: the sum of the bet and the stack of the poker player
        """
        return self.bet + self.stack

    @property
    def effective_stack(self: PokerPlayer) -> int:
        """Finds the effective stack of the poker player.

        The effective stack denotes how much a player can lose in a pot.

        :return: the effective stack of the poker player
        """
        return min(sorted(player.total for player in self.game.players)[-2], self.total)

    @property
    def relevant(self: PokerPlayer) -> bool:
        """Finds the relevancy of the poker player.

        A poker player is relevant if he/she can make a bet/raise and there is at least one opponent who can call.

        :return: the relevancy of the poker player
        """
        return not self.mucked and self.stack and self.effective_stack

    @property
    def hand(self: PokerPlayer) -> Hand:
        """
        :return: the hand of the poker player if any hand is made else None
        """
        return self.game._evaluator.hand(self.hole_cards, self.game.environment.board)

    @property
    def actions(self: PokerPlayer) -> list[PokerAction]:
        return self.game._round._create_actions()

    @property
    def payoff(self: PokerPlayer) -> int:
        return -self.commitment

    @property
    def __next__(self: PokerPlayer) -> Union[PokerNature, PokerPlayer]:
        player: Union[PokerNature, PokerPlayer] = super().__next__()

        while not player.relevant and player is not self.game.environment._aggressor:
            player: Union[PokerNature, PokerPlayer] = Player.__next__(player)

        return self.game.nature if player is self.game.environment._aggressor else player

    @property
    def _private_information(self: PokerPlayer) -> dict[str, Any]:
        return {
            **super()._private_information,
            'hole_cards': self.hole_cards,
        }

    @property
    def _public_information(self: PokerPlayer) -> dict[str, Any]:
        return {
            **super()._public_information,
            'bet': self.bet,
            'stack': self.stack,
            'hole_cards': None if self.hole_cards is None else [
                hole_card if hole_card.status else None for hole_card in self.hole_cards
            ],
        }


class PokerAction(SequentialAction[PokerGame, PokerEnvironment, PokerNature, PokerPlayer], ABC):
    """PokerAction is the abstract base class for all poker actions."""
    pass
