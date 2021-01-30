from typing import Generic, Sequence, TypeVar

from gameframe.poker.bases import PokerAction, PokerGame, PokerNature
from gameframe.poker.stages import BettingStage
from gameframe.poker.utils import Card, HoleCard

C = TypeVar('C', bound=Card, covariant=True)


class DealingAction(PokerAction[PokerNature], Generic[C]):
    def __init__(self, game: PokerGame, actor: PokerNature, cards: Sequence[C]):
        super().__init__(game, actor)

        self._cards = cards

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self._actor, PokerNature) \
               and isinstance(self._game.env._stage, BettingStage)


class HoleCardDealingAction(DealingAction[HoleCard]):
    def __init__(self, game: PokerGame, actor: PokerNature, cards: Sequence[HoleCard]):
        super().__init__(game, actor, cards)

    def __str__(self) -> str:
        return 'Deal ' + ', '.join(map(str, self._cards)) + ' hole cards'

    def act(self) -> None:
        super().act()

        count = 0

        for stage in self._game.env._stages[:self._game.env._stages.index(self)]:
            if isinstance(stage, BettingStage):
                count += len(stage._hole_card_statuses)

        player = next(player for player in self._game.players if len(player.hole_cards) != count)
        player._hole_cards.extend(self._cards)
        self._game.env._deck.remove(self._cards)

        if all(len(player.hole_cards) == count for player in self._game.players):
            self._game.env


class BoardCardDealingAction(DealingAction[Card]):
    def __str__(self) -> str:
        return 'Deal ' + ', '.join(map(str, self._cards)) + ' board cards'


class DistributingAction(PokerAction[PokerNature]):
    def __str__(self) -> str:
        return 'Distribute'
