from typing import Sequence, cast
from unittest import TestCase, main

from gameframe.poker import NLTexasHEGame, PokerPlayer, RedundancyException, StageException
from gameframe.poker.stages import DistributionStage, ShowdownStage
from gameframe.utils import pprint


class NLTexasHESimTestCase(TestCase):
    ANTE = 1
    BLINDS = 1, 2

    def test_not_betting_stage(self) -> None:
        self.assertRaises(StageException, lambda: self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs', 'Qc'],
                                                             'cccccccb2c', False).players[1].fold())
        self.assertRaises(StageException, lambda: self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs', 'Qc'],
                                                             'cccccccc', False).players[0].check_call())
        self.assertRaises(StageException, lambda: self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs', 'Qc'],
                                                             'cccccccb2b4c', False).players[0].bet_raise(100))
        self.assertRaises(StageException, lambda: self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                                                             ['AcAsKh', 'Qs', 'Qc'],
                                                             'cccccccccccccccb2ccc', False).players[3].fold())
        self.assertRaises(StageException, lambda: self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                                                             ['AcAsKh', 'Qs', 'Qc'],
                                                             'cccccccccccccccc', False).players[0].check_call())
        self.assertRaises(StageException, lambda: self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                                                             ['AcAsKh', 'Qs', 'Qc'],
                                                             'cccccccccccccccb2b4b6ccc', False).players[1].bet_raise(8))

    def test_redundant_fold(self) -> None:
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'cf')
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKh'], 'ccf')
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs'], 'cb4cccf')
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs', 'Qc'],
                          'cb4cccccf')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'], [],
                          'cccf')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                          ['AcAsKh'], 'b6ffcf')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                          ['AcAsKh', 'Qs'], 'cccccccccccf')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                          ['AcAsKh', 'Qs', 'Qc'], 'ffcccccccf')

    def test_redundant_bet_raise(self) -> None:
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b99b197')
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKh'], 'b6ccb93b193')
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs'],
                          'cb4ccccb95b195')
        self.assertRaises(RedundancyException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKh', 'Qs', 'Qc'],
                          'b6ccccccb93b193')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'], [],
                          'cccb99cb199cb299')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                          ['AcAsKh'], 'fb6fcb93b193')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                          ['AcAsKh', 'Qs'], 'cfcccccb197cb297')
        self.assertRaises(RedundancyException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKc', 'JsJd'],
                          ['AcAsKh', 'Qs', 'Qc'], 'cffcb10cb10b20cb67b267')

    def test_showdown_player(self) -> None:
        pass

    @classmethod
    def parse(cls, stacks: Sequence[int], hole_card_sets: Sequence[str], board_card_sets: Sequence[str],
              tokens: str, terminate: bool = True) -> NLTexasHEGame:
        game = NLTexasHEGame(cls.ANTE, cls.BLINDS, stacks)
        game.nature.setup()

        for player, hole_cards in zip(game.players, hole_card_sets):
            game.nature.deal_player(player, *(hole_cards[i:i + 2] for i in range(0, len(hole_cards), 2)))

        while tokens or board_card_sets:
            if isinstance(game.env.actor, PokerPlayer):
                token, tokens = tokens[0], tokens[1:]

                if token == 'b':
                    index = len(tokens) if tokens.isdigit() else next(
                        i for i in range(len(tokens)) if not tokens[i].isdigit())
                    amount, tokens = int(tokens[:index]), tokens[index:]
                    game.env.actor.bet_raise(amount)
                elif token == 'c':
                    game.env.actor.check_call()
                elif token == 'f':
                    game.env.actor.fold()
                else:
                    raise AssertionError
            else:
                cards, board_card_sets = ([board_card_sets[0][i:i + 2] for i in range(0, len(board_card_sets[0]), 2)],
                                          board_card_sets[1:])
                game.nature.deal_board(*cards)

        if terminate:
            while isinstance(game.env._stage, ShowdownStage):
                cast(PokerPlayer, game.env.actor).showdown()

            if isinstance(game.env._stage, DistributionStage):
                game.nature.distribute()

        return game


if __name__ == '__main__':
    main()
