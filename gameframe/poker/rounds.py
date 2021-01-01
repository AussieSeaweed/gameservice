from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from gameframe.poker.actions import AggressiveAction, PassiveAction, SubmissiveAction
from gameframe.poker.utils import HoleCard

if TYPE_CHECKING:
    from gameframe.poker import PokerAction, PokerGame, PokerNature, PokerPlayer


class Round(ABC):
    """Round is the abstract base class for all rounds."""

    def __init__(self: Round, game: PokerGame) -> None:
        self.__game: PokerGame = game

    @property
    def game(self: Round) -> PokerGame:
        """
        :return: the game of the round
        """
        return self.__game

    def _open(self: Round) -> None:
        self.game._actor = self._opener

    def _close(self: Round) -> None:
        self.game._actor = self.game.nature  # Redundant assignment, but just in case
        self.game._rounds.pop(0)

    @abstractmethod
    def _create_actions(self: Round) -> list[PokerAction]:
        pass

    @property
    @abstractmethod
    def _opener(self: Round) -> Union[PokerNature, PokerPlayer]:
        pass


class BettingRound(Round, ABC):
    """BettingRound is the abstract base class for all betting rounds."""

    def __init__(self: BettingRound, game: PokerGame, board_card_count: int, hole_card_statuses: list[bool],
                 lazy: bool) -> None:
        super(BettingRound, self).__init__(game)

        self.__board_card_count: int = board_card_count
        self.__hole_card_statuses: list[bool] = hole_card_statuses

        self.__lazy: bool = lazy

    def _open(self: BettingRound) -> None:
        super()._open()

        self.game.environment.board_cards.extend(self.game._deck.draw(self.__board_card_count))

        for player in self.game.players:
            if not player.mucked:
                for hole_card, status in zip(self.game._deck.draw(len(self.__hole_card_statuses)),
                                             self.__hole_card_statuses):
                    player.hole_cards.append(HoleCard(hole_card, status))

        if self.game.actor.nature:
            self._close()
        else:
            self.game.environment._aggressor = self.game.actor
            self.game.environment._max_delta = max(self.game.blinds)

    @property
    def _opener(self: BettingRound) -> Union[PokerNature, PokerPlayer]:
        if any(player.bet for player in self.game.players):
            opener = self.game.players[1 if len(self.game.players) == 2 else 2]

            return opener if opener.relevant else next(opener)
        else:
            try:
                return next(player for player in self.game.players if player.relevant)
            except StopIteration:
                return self.game.nature

    def _close(self: BettingRound) -> None:
        super()._close()

        self.game.environment._max_delta = None
        self.game.environment._pot += sum(player.bet for player in self.game.players)

        for player in self.game.players:
            player._bet = 0

    def _create_actions(self: BettingRound) -> list[PokerAction]:
        actions = []

        if self.game.actor.bet < max(player.bet for player in self.game.players):
            actions.append(SubmissiveAction(self.game.actor))

        actions.append(PassiveAction(self.game.actor))

        if sum(player.relevant for player in self.game.players) > 1 and \
                max(player.bet for player in self.game.players) < self.game.actor.stack:
            if self.__lazy:
                actions.extend([
                    AggressiveAction(self.game.actor, self._min_amount),
                    AggressiveAction(self.game.actor, self._max_amount),
                ])
            else:
                actions.extend(map(lambda amount: AggressiveAction(self.game.actor, amount),
                                   range(self._min_amount, self._max_amount + 1)))

        return actions

    @property
    def _min_amount(self) -> int:
        return min(max(player.bet for player in self.game.players) + self.game.environment._max_delta,
                   self.game.actor.total)

    @property
    @abstractmethod
    def _max_amount(self) -> int:
        pass


class NoLimitBettingRound(BettingRound):
    """NoLimitBettingRound is the class for no-limit betting rounds."""

    @property
    def _max_amount(self) -> int:
        return self.game.actor.total


class LimitBettingRound(BettingRound):
    """LimitBettingRound is the class for limit betting rounds."""

    @property
    def _max_amount(self) -> int:
        return self._min_amount
