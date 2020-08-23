from __future__ import annotations

from abc import ABC
from typing import Optional, Dict, List, TYPE_CHECKING, Any

from gameservice.sequential.game import Action

if TYPE_CHECKING:
    from .game import PokerGame


# Player Actions


class Put(Action, ABC):
    amount: int

    def valid(self, game: PokerGame) -> bool:
        pass

    def apply(self, game: PokerGame) -> None:
        super().apply(game)


class NoLimitPut(Put):
    def __init__(self, amount: int, *args):
        super().__init__(*args)

        self.amount: int = amount

    @classmethod
    def info(cls, game: PokerGame) -> Optional[Dict]:
        pass


class Continue(Action):
    @classmethod
    def info(cls, game: PokerGame) -> Optional[Dict[str, Any]]:
        pass

    def valid(self, game: PokerGame) -> bool:
        pass

    def apply(self, game: PokerGame) -> None:
        super().apply(game)


class Surrender(Action):
    @classmethod
    def info(cls, game: PokerGame) -> Optional[Dict[str, Any]]:
        pass

    def valid(self, game: PokerGame) -> bool:
        pass

    def apply(self, game: PokerGame) -> None:
        super().apply(game)


# Nature actions


class Deal(Action):
    def __init__(self, exposure_list: List[bool], *args):
        super().__init__(*args)

        self.exposure_list: List[bool] = exposure_list

    @classmethod
    def info(cls, game: PokerGame) -> Optional[Dict[str, Any]]:
        return None

    def valid(self, game: PokerGame) -> bool:
        return game.turn is None

    def apply(self, game: PokerGame) -> None:
        super().apply(game)

        for player in game.players:
            if player is not None:
                player.cards.extend(player.Card(card_str, exposed) for card_str, exposed in
                                    zip(game.deck.draw(self.num_dealt), self.exposure_list))

    @property
    def num_dealt(self):
        return len(self.exposure_list)


class Peel(Action):
    pass


class Showdown(Action):
    pass
