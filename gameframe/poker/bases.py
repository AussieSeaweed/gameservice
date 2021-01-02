from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional, TYPE_CHECKING, Union

from gameframe.game import Environment, Nature, Player
from gameframe.sequential import SequentialAction, SequentialGame

if TYPE_CHECKING:
    from gameframe.poker import Card, Deck, Evaluator, Hand, HoleCard, Round, Limit


class PokerGame(SequentialGame['PokerGame', 'PokerEnvironment', 'PokerNature', 'PokerPlayer'], ABC):
    """PokerGame is the abstract base class for all poker games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self) -> None:
        super().__init__()

        if not len(self.players) > 1:
            raise ValueError('Poker is played by more than 2 players')

        self._deck: Deck = self._create_deck()
        self._evaluator: Evaluator = self._create_evaluator()
        self._limit: Limit = self._create_limit()
        self._rounds: list[Round] = self._create_rounds()

        self._setup()

    @property
    @abstractmethod
    def ante(self) -> int:
        """
        :return: the ante of the poker game
        """
        pass

    @property
    @abstractmethod
    def blinds(self) -> list[int]:
        """
        :return: the blinds of the poker game
        """
        pass

    @property
    @abstractmethod
    def starting_stacks(self) -> list[int]:
        """
        :return: the starting stacks of the poker game
        """
        pass

    @property
    def _information(self) -> dict[str, Any]:
        return {
            **super()._information,
            'ante': self.ante,
            'blinds': self.blinds,
            'starting_stacks': self.starting_stacks,
        }

    @property
    def _initial_actor(self) -> PokerNature:
        return self.nature

    @property
    def _round(self) -> Round:
        return self._rounds[0] if self._rounds else None

    @property
    @abstractmethod
    def _lazy(self) -> bool:
        pass

    def _create_environment(self) -> PokerEnvironment:
        return PokerEnvironment(self)

    def _create_nature(self) -> PokerNature:
        return PokerNature(self)

    def _create_players(self) -> list[PokerPlayer]:
        return [PokerPlayer(self, starting_stack) for starting_stack in self.starting_stacks]

    def _setup(self) -> None:
        for player in self.players:
            ante: int = min(self.ante, player.stack)

            player._stack -= ante
            self.environment._pot += ante

        for player, blind in zip(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds):
            blind: int = min(blind, player.stack)

            player._stack -= blind
            player._bet += blind

    @abstractmethod
    def _create_deck(self) -> Deck:
        pass

    @abstractmethod
    def _create_evaluator(self) -> Evaluator:
        pass

    @abstractmethod
    def _create_limit(self) -> Limit:
        pass

    @abstractmethod
    def _create_rounds(self) -> list[Round]:
        pass


class PokerEnvironment(Environment[PokerGame, 'PokerEnvironment', 'PokerNature', 'PokerPlayer']):
    """PokerEnvironment is the class for poker environments."""

    def __init__(self, game: PokerGame) -> None:
        super().__init__(game)

        self._aggressor: Optional[PokerPlayer] = None
        self._max_delta: Optional[int] = None
        self._pot: int = 0
        self.__board_cards: list[Card] = []

    @property
    def board_cards(self) -> list[Card]:
        """
        :return: the board cards of the poker environment
        """
        return self.__board_cards

    @property
    def pot(self) -> int:
        """
        :return: the pot of the poker environment
        """
        return self._pot

    @property
    def _information(self) -> dict[str, Any]:
        return {
            **super()._information,
            'pot': self.pot,
            'board_cards': self.board_cards,
        }


class PokerNature(Nature[PokerGame, PokerEnvironment, 'PokerNature', 'PokerPlayer']):
    """PokerNature is the class for poker natures."""

    @property
    def actions(self) -> list[PokerAction]:
        from gameframe.poker import RoundAction

        return [RoundAction(self)] if self is self.game.actor else []

    @property
    def payoff(self) -> int:
        return 0


class PokerPlayer(Player[PokerGame, PokerEnvironment, PokerNature, 'PokerPlayer']):
    """PokerPlayer is the class for poker players."""

    def __init__(self, game: PokerGame, starting_stack: int) -> None:
        super().__init__(game)

        self._bet: int = 0
        self._stack: int = 0
        self.__hole_cards: Optional[list[HoleCard]] = []
        self.__starting_stack: int = starting_stack

    @property
    def actions(self) -> list[PokerAction]:
        return self.game._round._create_actions() if self is self.game.actor else []

    @property
    def bet(self) -> int:
        """
        :return: the bet of the poker player
        """
        return self._bet

    @property
    def commitment(self) -> int:
        """
        :return: the amount the poker player has put
        """
        return self.__starting_stack - self.stack

    @property
    def effective_stack(self) -> int:
        """Finds the effective stack of the poker player.

        The effective stack denotes how much a player can lose.

        :return: the effective stack of the poker player
        """
        try:
            return min(sorted(player.total for player in self.game.players if not player.mucked)[-2], self.total)
        except IndexError:
            return 0

    @property
    def hand(self) -> Hand:
        """
        :return: the hand of the poker player if any hand is made else None
        """
        return self.game._evaluator.hand(self.hole_cards, self.game.environment.board_cards)

    @property
    def hole_cards(self) -> Optional[list[HoleCard]]:
        """
        :return: the hole cards of the poker player
        """
        return self.__hole_cards

    @property
    def mucked(self) -> bool:
        """
        :return: True if the poker player has mucked, False otherwise
        """
        return self.hole_cards is None

    @property
    def payoff(self) -> int:
        return -self.commitment

    @property
    def relevant(self) -> bool:
        """Finds the relevancy of the poker player.

        A poker player is relevant if he/she can make a bet/raise and be played back.

        :return: the relevancy of the poker player
        """
        return not self.mucked and self.stack and self.effective_stack

    @property
    def stack(self) -> int:
        """
        :return: the stack of the poker player
        """
        return self._stack

    @property
    def total(self) -> int:
        """
        :return: the sum of the bet and the stack of the poker player
        """
        return self.bet + self.stack

    def __lt__(self, other: PokerPlayer) -> bool:
        return self.commitment < other.commitment if self.hand == other.hand else self.hand > other.hand

    def __next__(self) -> Union[PokerNature, PokerPlayer]:
        player: Union[PokerNature, PokerPlayer] = super().__next__()

        while not player.relevant and player is not self.game.environment._aggressor:
            player: Union[PokerNature, PokerPlayer] = Player.__next__(player)

        return self.game.nature if player is self.game.environment._aggressor else player

    @property
    def _private_information(self) -> dict[str, Any]:
        return {
            **super()._private_information,
            'hole_cards': self.hole_cards,
        }

    @property
    def _public_information(self) -> dict[str, Any]:
        return {
            **super()._public_information,
            'bet': self.bet,
            'stack': self.stack,
            'hole_cards': None if self.hole_cards is None else map(
                lambda hole_card: hole_card if hole_card.status else None,
                self.hole_cards,
            ),
        }

    def _muck(self) -> None:
        self.__hole_cards: Optional[list[HoleCard]] = None


class PokerAction(SequentialAction[PokerGame, PokerEnvironment, PokerNature, PokerPlayer], ABC):
    """PokerAction is the abstract base class for all poker actions."""

    @property
    def public(self) -> bool:
        return True


class PokerPlayerAction(PokerAction, ABC):
    """PokerPlayerAction is the abstract base class for all poker player actions."""

    @property
    def chance(self) -> bool:
        return False


class PokerNatureAction(PokerAction, ABC):
    """PokerNatureAction is the abstract base class for all poker nature actions."""

    @property
    def chance(self) -> bool:
        return True
