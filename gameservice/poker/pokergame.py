from abc import ABC, abstractmethod

from .pokerplayer import PokerPlayer, PokerNature
from .pokerutils import PokerStreet, PokerStdDeck, PokerStdEvaluator, PokerNoLimit, PokerLazyNoLimit
from ..game import SequentialGame, GamePlayerException, GameParameterException


class PokerGame(SequentialGame, ABC):
    def __init__(self):
        super().__init__()

        if not len(self.starting_stacks) > 1:
            raise GamePlayerException('Poker is played by more than 2 players')

        self.__streets = self._create_streets()
        self.__deck = self._create_deck()
        self.__evaluator = self._create_evaluator()
        self.__limit = self._create_limit()

        self.aggressor = None
        self.min_raise = None

        self.pot = 0
        self.__board = []

        self.setup()

    def _create_players(self):
        return [PokerPlayer(self, i) for i in range(len(self.starting_stacks))]

    def _create_nature(self):
        return PokerNature(self)

    @property
    def _initial_player(self):
        return self.nature

    @abstractmethod
    def _create_streets(self):
        pass

    @abstractmethod
    def _create_deck(self):
        pass

    @abstractmethod
    def _create_evaluator(self):
        pass

    @abstractmethod
    def _create_limit(self):
        pass

    @property
    @abstractmethod
    def starting_stacks(self):
        pass

    @property
    @abstractmethod
    def blinds(self):
        pass

    @property
    @abstractmethod
    def ante(self):
        pass

    @property
    def streets(self):
        return self.__streets

    @property
    def street(self):
        return self.__streets[0] if self.__streets else None

    @property
    def deck(self):
        return self.__deck

    @property
    def evaluator(self):
        return self.__evaluator

    @property
    def limit(self):
        return self.__limit

    @property
    def board(self):
        return self.__board

    def setup(self):
        for player in self.players:
            ante = min(self.ante, player.stack)

            player.stack -= ante
            self.pot += ante

        for player, blind in zip(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds):
            blind = min(blind, player.stack)

            player.stack -= blind
            player.bet += blind


class NLHEGame(PokerGame, ABC):
    def __init__(self):
        super().__init__()

        if len(self.blinds) != 2 or self.blinds[0] >= self.blinds[1]:
            raise GameParameterException('The blinds have to be length of 2 and be sorted')

    def _create_streets(self):
        return [PokerStreet(2, 0), PokerStreet(0, 3), PokerStreet(0, 1), PokerStreet(0, 1)]

    def _create_deck(self):
        return PokerStdDeck()

    def _create_evaluator(self):
        return PokerStdEvaluator()

    def _create_limit(self):
        return PokerNoLimit()


class LazyNLHEGame(NLHEGame, ABC):
    def _create_limit(self):
        return PokerLazyNoLimit()
