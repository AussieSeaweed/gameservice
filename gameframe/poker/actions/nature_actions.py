from itertools import zip_longest
from typing import Generic, Sequence, TypeVar, cast

from gameframe.poker.bases import PokerAction, PokerGame, PokerNature, PokerPlayer
from gameframe.poker.rounds import DealingRound, SetupRound, ShowdownRound
from gameframe.poker.utils import Card, HoleCard

C = TypeVar('C', bound=Card)


class SetupAction(PokerAction[PokerNature], Generic[C]):
    """SetupAction is the class for game setups."""

    def __repr__(self) -> str:
        return 'Set up'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self.actor, PokerNature) \
               and isinstance(self.game.env._round, SetupRound)

    def act(self) -> None:
        super().act()

        blinds = list(reversed(self.game.env.blinds)) if len(self.game.players) == 2 else self.game.env.blinds

        for player, blind in zip_longest(self.game.players, blinds, fillvalue=0):
            player._commitment = min(self.game.env.ante + blind, player._total)

        self.game.env._requirement = self.game.env.ante

        self._change_round()


class DealingAction(PokerAction[PokerNature], Generic[C]):
    """DealingAction is the class for card dealings."""

    def __init__(self, game: PokerGame, actor: PokerNature, cards: Sequence[C]):
        super().__init__(game, actor)

        self._cards = cards

    def __repr__(self) -> str:
        return 'Deal (' + ', '.join(map(str, self._cards)) + ')'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self.actor, PokerNature) \
               and isinstance(self.game.env._round, DealingRound) \
               and all(card in self.game.env._deck for card in self._cards)

    def act(self) -> None:
        super().act()

        self.game.env._deck.remove(self._cards)


class HoleCardDealingAction(DealingAction[HoleCard]):
    """HoleCardDealingAction is the class for hole card dealings."""

    def __repr__(self) -> str:
        return super().__repr__() + ' as hole cards'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable \
               and any(len(player.hole_cards) < cast(DealingRound, self.game.env._round)._target_hole_card_count
                       for player in self.game.players if not player.is_mucked)

    def act(self) -> None:
        super().act()

        active_players = list(filter(lambda player: not player.is_mucked, self.game.players))
        hole_card_count = min(len(player.hole_cards) for player in active_players)

        player = next(player for player in active_players if len(player.hole_cards) == hole_card_count)
        player._hole_cards.extend(self._cards)


class BoardCardDealingAction(DealingAction[Card]):
    """BoardCardDealingAction is the class for board card dealings."""

    def __repr__(self) -> str:
        return super().__repr__() + ' as board cards'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable \
               and any(len(player.hole_cards) == cast(DealingRound, self.game.env._round)._target_hole_card_count
                       for player in self.game.players if not player.is_mucked) \
               and len(self.game.env.board_cards) < cast(DealingRound, self.game.env._round)._target_board_card_count

    def act(self) -> None:
        super().act()

        self.game.env._board_cards.extend(self._cards)

        self._change_round()


class DistributionAction(PokerAction[PokerNature]):
    """DistributionAction is the class for pot distributions."""

    def __repr__(self) -> str:
        return 'Distribute'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self.actor, PokerNature) \
               and isinstance(self.game.env._round, ShowdownRound)

    def act(self) -> None:
        super().act()

        players = list(filter(lambda p: not p.is_mucked, self.game.players))
        base = 0

        for player in sorted(players, key=lambda p: (p.hand, -p._commitment), reverse=True):
            side_pot = self.__side_pot(base, player)

            recipients = list(filter(lambda p: p.hand == player.hand, players))

            for recipient in recipients:
                recipient._total += side_pot // len(recipients)
            else:
                recipients[0]._total += side_pot % len(recipients)

            base = max(base, player._commitment)

        self.game.env._actor = None

    def __side_pot(self, base: int, base_player: PokerPlayer) -> int:
        side_pot = 0

        for player in self.game.players:
            entitlement = min(player._commitment, base_player._commitment)

            if base < entitlement:
                side_pot += entitlement - base

        return side_pot
