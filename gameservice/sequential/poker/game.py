from abc import ABC
from typing import List, Type, TYPE_CHECKING

from ..game import SequentialGame
from gameservice.exceptions import TerminalError

if TYPE_CHECKING:
    from gameservice.util.poker import PokerDeck
    from .street import Street
    from .player import PokerPlayer


class PokerGame(SequentialGame, ABC):
    """
    A class for poker games
    """

    """Poker game type checking helpers"""

    players: List[PokerPlayer]

    """Poker game member variable overrides"""

    min_num_players = 2

    """Poker game member variables"""

    deck_type: Type[PokerDeck]
    street_types: List[Type[Street]]

    def __init__(self, num_players: int):
        super().__init__(num_players)

        self.deck: PokerDeck = self._create_deck()
        self.streets: List[Street] = self._create_streets()
        self.street_index: int = 0

    """Protected member functions"""

    def _create_deck(self) -> PokerDeck:
        return self.deck_type()

    def _create_streets(self) -> List[Street]:
        return [street_type() for street_type in self.street_types]

    """Public member functions"""

    @property
    def street(self) -> Street:
        try:
            return self.streets[self.street_index]
        except IndexError:
            raise TerminalError
