from abc import ABC
from itertools import repeat
from random import sample
from typing import Generic, cast
from unittest import TestCase, main

from auxiliary import ExtendedTestCase
from pokertools import parse_cards

from gameframe.exceptions import GameFrameError
from gameframe.game import _G
from gameframe.poker import (BetRaiseAmountException, BettingStage, BoardDealingStage, FixedLimitBadugi,
                             FixedLimitGreekHoldEm, HoleDealingStage, KuhnPoker, NoLimitFiveCardDraw,
                             NoLimitShortHoldEm, NoLimitTexasHoldEm, Poker, PokerPlayer, PotLimitOmahaHoldEm,
                             parse_poker)
from gameframe.poker.parameters import _ShowdownStage
from gameframe.tictactoe import TicTacToe, parse_tic_tac_toe


class SimulationTestCaseMixin(Generic[_G], ABC):
    pass



if __name__ == '__main__':
    main()
