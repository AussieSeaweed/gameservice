"""
This module defines poker games in gameservice.
"""
from abc import ABC, abstractmethod

from .environments import PokerEnvironment
from .players import PokerNature, PokerPlayer
from .utils import LazyNoLimit, NoLimit, StandardDeck, StandardEvaluator, Street
from ..game import ParameterException, SequentialGame


class PokerGame(SequentialGame, ABC):
    """
    This is a class that represents poker games.
    """

    def __init__(self):
        """
        Constructs a PokerGame instance. Initializes the deck, evaluator, limit, and streets.

        :raise ParameterException: if the number of players is less than 2
        """
        super().__init__()

        if not len(self.starting_stacks) > 1:
            raise ParameterException('Poker is played by more than 2 players')

        self.__deck = self._create_deck()
        self.__evaluator = self._create_evaluator()
        self.__limit = self._create_limit()
        self.__streets = self._create_streets()

        self.setup()

    def create_environment(self):
        """
        Creates a poker environment.

        :return: a poker environment
        """
        return PokerEnvironment(self)

    def create_nature(self):
        """
        Creates a poker nature.

        :return: a poker nature
        """
        return PokerNature(self)

    def create_player(self):
        """
        Creates poker players.

        :return: a list of poker players
        """
        return [PokerPlayer(self, i) for i in range(len(self.starting_stacks))]

    @property
    def _initial_player(self):
        """
        :return: the initial player of the poker game
        """
        return self.nature

    @abstractmethod
    def _create_deck(self):
        """
        Creates a poker deck.

        :return: a poker deck
        """
        pass

    @abstractmethod
    def _create_evaluator(self):
        """
        Creates a poker evaluator.

        :return: a poker evaluator
        """
        pass

    @abstractmethod
    def _create_limit(self):
        """
        Creates a poker limit.

        :return: a poker limit
        """
        pass

    @abstractmethod
    def _create_streets(self):
        """
        Creates poker streets.

        :return: a list of poker streets
        """
        pass

    @property
    def deck(self):
        """
        :return: the deck of the poker game
        """
        return self.__deck

    @property
    def evaluator(self):
        """
        :return: the evaluator of the poker game
        """
        return self.__evaluator

    @property
    def limit(self):
        """
        :return: the limit of the poker game
        """
        return self.__limit

    @property
    def streets(self):
        """
        :return: a list of the streets of the poker game
        """
        return self.__streets

    @property
    def street(self):
        """
        :return: the street of the poker game
        """
        return self.__streets[0] if self.__streets else None

    @property
    @abstractmethod
    def ante(self):
        """
        :return: the ante of the poker game
        """
        pass

    @property
    @abstractmethod
    def blinds(self):
        """
        :return: the blinds of the poker game
        """
        pass

    @property
    @abstractmethod
    def starting_stacks(self):
        """
        :return: the starting stacks of the poker game
        """
        pass

    def setup(self):
        """
        Takes antes and blinds the players.

        :return: None
        """
        for player in self.players:
            ante = min(self.ante, player.stack)

            player.stack -= ante
            self.environment.pot += ante

        for player, blind in zip(self.players, reversed(self.blinds) if len(self.players) == 2 else self.blinds):
            blind = min(blind, player.stack)

            player.stack -= blind
            player.bet += blind


class NLHEGame(PokerGame, ABC):
    """
    This is a class that represents no-limit texas hold'em games.
    """

    def __init__(self):
        """
        Constructs a NLHEGame instance.

        :raise ParameterException: if the blinds are invalid
        """
        super().__init__()

        if len(self.blinds) != 2 or self.blinds[0] >= self.blinds[1]:
            raise ParameterException('The blinds have to be length of 2 and be sorted')

    def _create_deck(self):
        """
        Creates a deck of the no-limit texas hold'em game.

        :return: a deck of the no-limit texas hold'em game.
        """
        return StandardDeck()

    def _create_evaluator(self):
        """
        Creates an evaluator of the no-limit texas hold'em game.

        :return: an evaluator of the no-limit texas hold'em game.
        """
        return StandardEvaluator()

    def _create_limit(self):
        """
        Creates a limit of the no-limit texas hold'em game.

        :return: a limit of the no-limit texas hold'em game.
        """
        return NoLimit()

    def _create_streets(self):
        """
        Creates streets of the no-limit texas hold'em game.

        :return: a list of streets of the no-limit texas hold'em game.
        """
        return [Street(2, 0), Street(0, 3), Street(0, 1), Street(0, 1)]


class LazyNLHEGame(NLHEGame, ABC):
    """
    This is a class that represents lazy no-limit texas hold'em games. Unlike no-limit texas hold'em games, the actions
    generated by each player only contains minimum and maximum bet amount. To bet/raise an amount that is neither
    minimum or maximum, an AggressiveAction instance should be created and used.
    """

    def _create_limit(self):
        """
        Creates a limit of the lazy no-limit texas hold'em game.

        :return: a limit of the lazy no-limit texas hold'em game.
        """
        return LazyNoLimit()
