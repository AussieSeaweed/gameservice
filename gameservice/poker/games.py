from abc import ABC, abstractmethod

from .environments import PokerEnvironment
from .players import PokerNature, PokerPlayer
from .utils import LazyNoLimit, NoLimit, StandardDeck, StandardEvaluator, Street
from ..game import ParameterException, SeqGame


class PokerGame(SeqGame, ABC):
    def __init__(self):
        super().__init__()

        if not len(self.starting_stacks) > 1:
            raise ParameterException('Poker is played by more than 2 players')

        self.__deck = self._create_deck()
        self.__evaluator = self._create_evaluator()
        self.__limit = self._create_limit()
        self.__streets = self._create_streets()

        self.setup()

    def _create_environment(self):
        return PokerEnvironment(self)

    def _create_nature(self):
        return PokerNature(self)

    def _create_players(self):
        return [PokerPlayer(self, i) for i in range(len(self.starting_stacks))]

    @property
    def _initial_player(self):
        return self.nature

    @abstractmethod
    def _create_deck(self):
        pass

    @abstractmethod
    def _create_evaluator(self):
        pass

    @abstractmethod
    def _create_limit(self):
        pass

    @abstractmethod
    def _create_streets(self):
        pass

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
    def streets(self):
        return self.__streets

    @property
    def street(self):
        return self.__streets[0] if self.__streets else None

    @property
    @abstractmethod
    def ante(self):
        pass

    @property
    @abstractmethod
    def blinds(self):
        pass

    @property
    @abstractmethod
    def starting_stacks(self):
        pass

    def setup(self):
        for player in self.players:
            ante = min(self.ante, player.stack)

            player.stack -= ante
            self.environment.pot += ante

        for player, blind in zip(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds):
            blind = min(blind, player.stack)

            player.stack -= blind
            player.bet += blind


class NLHEGame(PokerGame, ABC):
    def __init__(self):
        super().__init__()

        if len(self.blinds) != 2 or self.blinds[0] >= self.blinds[1]:
            raise ParameterException('The blinds have to be length of 2 and be sorted')

    def _create_deck(self):
        return StandardDeck()

    def _create_evaluator(self):
        return StandardEvaluator()

    def _create_limit(self):
        return NoLimit()

    def _create_streets(self):
        return [Street(2, 0), Street(0, 3), Street(0, 1), Street(0, 1)]


class LazyNLHEGame(NLHEGame, ABC):
    def _create_limit(self):
        return LazyNoLimit()
