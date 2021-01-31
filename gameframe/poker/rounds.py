from abc import ABC, abstractmethod
from itertools import combinations
from typing import Generic, MutableSequence, Sequence, Union, cast

from gameframe.poker.bases import A, BaseRound, PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.utils import HoleCard
from gameframe.utils import rotate


class Round(BaseRound, Generic[A], ABC):
    @property
    @abstractmethod
    def actions(self) -> Sequence[PokerAction[A]]:
        pass


class NatureRound(Round[PokerNature], ABC):
    pass


class PlayerRound(Round[PokerPlayer], ABC):
    pass


class RoundOpenMixin(ABC):
    @abstractmethod
    def open(self) -> None:
        pass


class RoundCloseMixin(ABC):
    @abstractmethod
    def close(self) -> None:
        pass


class SetupRound(NatureRound):
    @property
    def actions(self) -> Sequence[PokerAction[PokerNature]]:
        from gameframe.poker.actions import SetupAction

        return [SetupAction(self.game, self.game.nature)]


class DealingRound(NatureRound):
    def __init__(self, game: PokerGame, hole_card_statuses: Sequence[bool], board_card_count: int):
        super().__init__(game)

        self.__hole_card_statuses = hole_card_statuses
        self.__board_card_count = board_card_count

    @property
    def actions(self) -> Sequence[PokerAction[PokerNature]]:
        from gameframe.poker.actions import HoleCardDealingAction, BoardCardDealingAction

        actions: MutableSequence[PokerAction[PokerNature]] = []

        if all(player.is_mucked or len(player.hole_cards) == self._target_hole_card_count
               for player in self.game.players):
            for combination in combinations(self.game.env._deck, self.__board_card_count):
                actions.append(BoardCardDealingAction(self.game, self.game.nature, combination))
        else:
            # TODO: Getting combination does not account for all possibilities, so fix
            # When hole card statuses are not of the same values, the order of hole cards dealt matters
            # this is okay for hold'em games where all hole cards are dealt face down
            for combination in combinations(self.game.env._deck, len(self.__hole_card_statuses)):
                hole_cards: MutableSequence[HoleCard] = []

                for card, status in zip(combination, self.__hole_card_statuses):
                    hole_cards.append(HoleCard(card, status))

                actions.append(HoleCardDealingAction(self.game, self.game.nature, hole_cards))

        return actions

    @property
    def _target_hole_card_count(self) -> int:
        count = len(self.__hole_card_statuses)

        for rnd in self.game.env._rounds[:self.game.env._rounds.index(self)]:
            if isinstance(rnd, DealingRound):
                count += len(rnd.__hole_card_statuses)

        return count

    @property
    def _target_board_card_count(self) -> int:
        count = self.__board_card_count

        for rnd in self.game.env._rounds[:self.game.env._rounds.index(self)]:
            if isinstance(rnd, DealingRound):
                count += rnd.__board_card_count

        return count

    def open(self) -> None:
        self.game.env._actor = self.game.nature


class DistributionRound(NatureRound, RoundOpenMixin):
    @property
    def actions(self) -> Sequence[PokerAction[PokerNature]]:
        from gameframe.poker.actions import DistributionAction

        return [DistributionAction(self.game, self.game.nature)]

    def open(self) -> None:
        self.game.env._actor = self.game.nature


class BettingRound(PlayerRound, RoundOpenMixin, RoundCloseMixin, ABC):
    @property
    def min_amount(self) -> int:
        player = cast(PokerPlayer, self.game.env.actor)

        return min(max(p.bet for p in self.game.players) + self.game.env._max_delta, player.bet + player.stack)

    @property
    @abstractmethod
    def max_amount(self) -> int:
        pass

    @property
    def actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        from gameframe.poker.actions import BetRaiseAction, CheckCallAction, FoldAction

        player = cast(PokerPlayer, self.game.env.actor)
        actions = [FoldAction(self.game, player), CheckCallAction(self.game, player)]

        for amount in range(self.min_amount, self.max_amount + 1):
            actions.append(BetRaiseAction(self.game, player, amount))

        return list(filter(lambda action: action.is_applicable, actions))

    @property
    def opener(self) -> Union[PokerNature, PokerPlayer]:
        opener = min(self.game.players, key=lambda p: (p.bet, self.game.players.index(p)))

        for opener in rotate(self.game.players, self.game.players.index(opener)):
            if opener._is_relevant:
                return opener
        else:
            return self.game.nature

    @property
    def initial_max_delta(self) -> int:
        return max(self.game.env.ante, max(self.game.env.blinds))

    def open(self) -> None:
        self.game.env._actor = self.opener

        if isinstance(self.game.env._actor, PokerPlayer):
            self.game.env._max_delta = self.initial_max_delta
            self.game.env._aggressor = self.game.env._actor

    def close(self) -> None:
        self.game.env._requirement = max(player._commitment for player in self.game.players)


class NLBettingRound(BettingRound):
    @property
    def max_amount(self) -> int:
        player = cast(PokerPlayer, self.game.env.actor)

        return player.bet + player.stack


class ShowdownRound(PlayerRound, RoundOpenMixin):
    @property
    def actions(self) -> Sequence[PokerAction[PokerPlayer]]:
        from gameframe.poker.actions import ShowdownAction

        player = cast(PokerPlayer, self.game.env.actor)

        return [ShowdownAction(self.game, player, False), ShowdownAction(self.game, player, True)]

    def open(self) -> None:
        self.game.env._actor = self.game.env._aggressor
