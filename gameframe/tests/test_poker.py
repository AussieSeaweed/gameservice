from abc import ABC

from gameframe.poker import Poker
from gameframe.tests import GameFrameTestCaseMixin


class PokerTestMixin(GameFrameTestCaseMixin[Poker], ABC):
    ...
