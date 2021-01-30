from abc import ABC, abstractmethod
from typing import MutableSequence, Sequence, Union

from gameframe.poker.actions import BetRaiseAction, BettingAction, CheckCallAction, FoldAction
from gameframe.poker.utils import HoleCard
from gameframe.poker.bases import PokerGame, PokerAction, PokerNature, PokerPlayer
from gameframe.poker.exceptions import IllegalStateException
from gameframe.utils import rotate


class Round(ABC):
    """Round is the abstract base class for all rounds."""

    def __init__(self, game: PokerGame):
        self._game = game

    @property
    @abstractmethod
    def actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        """
        :return: the actions of this round
        """
        pass

    @property
    @abstractmethod
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        """
        :return: the opener of this round
        """
        pass

    @property
    def _player(self) -> PokerPlayer:
        if isinstance(self._game.env.actor, PokerPlayer):
            return self._game.env.actor
        else:
            raise IllegalStateException()

    @abstractmethod
    def open(self) -> None:
        """Opens this round.

        :return: None
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """Closes this round.

        :return: None
        """
        pass


class BettingRound(Round, ABC):
    """BettingRound is the class for betting rounds."""

    def __init__(self, game: PokerGame, board_card_count: int, hole_card_statuses: Sequence[bool]):
        super().__init__(game)

        self.__board_card_count = board_card_count
        self.__hole_card_statuses = hole_card_statuses

    @property
    def actions(self) -> Sequence[BettingAction]:
        actions = [FoldAction(self._game, self._player), CheckCallAction(self._game, self._player)]

        for amount in range(self._game.env._limit.min_amount(self._player),
                            self._game.env._limit.max_amount(self._player) + 1):
            actions.append(BetRaiseAction(self._game, self._player, amount))

        return list(filter(lambda action: action.is_applicable, actions))

    @property
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        opener = min(self._game.players, key=lambda player: (player.bet, self._game.players.index(player)))

        for opener in rotate(self._game.players, self._game.players.index(opener)):
            if opener._is_relevant:
                return opener
        else:
            return self._game.nature

    def open(self) -> None:
        dealt_cards = list(self._game.env._deck)[:self.__board_card_count]
        self._game.env._board_cards.extend(dealt_cards)

        for player in self._game.players:
            if not player.is_mucked:
                hole_cards: MutableSequence[HoleCard] = []

                for card, status in zip(tuple(self._game.env._deck)[:len(self.__hole_card_statuses)],
                                        self.__hole_card_statuses):
                    hole_cards.append(HoleCard(card, status))

                dealt_cards.extend(hole_cards)

                if player._hole_cards is not None:
                    player._hole_cards.extend(hole_cards)

        self._game.env._deck.remove(dealt_cards)

        if isinstance(self.opener, PokerPlayer):
            self._game.env._max_delta = max(self._game._ante, max(self._game._blinds))
            self._game.env._aggressor = self.opener

    def close(self) -> None:
        self._game.env._max_delta = 0
        self._game.env._requirement = max(player._commitment for player in self._game.players)
