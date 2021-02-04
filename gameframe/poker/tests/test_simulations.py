from typing import Optional, Sequence, cast
from unittest import TestCase, main

from gameframe.game import ActionException
from gameframe.poker import NLTHEGame, PokerGame, PokerPlayer
from gameframe.poker.stages import ShowdownStage


class NLTexasHESimTestCase(TestCase):
    ANTE = 1
    BLINDS = 1, 2

    def test_not_betting_stage(self) -> None:
        self.assertRaises(ActionException, self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccccccb2c', False).players[1].fold)
        self.assertRaises(ActionException, self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccccccc', False).players[0].check_call)
        self.assertRaises(ActionException, self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccccccb2b4c', False).players[0].bet_raise, 100)
        self.assertRaises(ActionException, self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                                                      ['AcAsKc', 'Qs', 'Qc'], 'cccccccccccccccb2ccc').players[0].fold)
        self.assertRaises(ActionException, self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                                                      ['AcAsKc', 'Qs', 'Qc'], 'cccccccccccccccc').players[0].check_call)
        self.assertRaises(ActionException, self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                                                      ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccccccccccccccb2b4b6ccc').players[1].bet_raise, 8)

    def test_redundant_fold(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'cf')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'ccf')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'], 'cb4cccf')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'cb4cccccf')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'cccf')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'b6ffcf')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'cccccccccccf')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'ffcccccccf')

    def test_covered_stack(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b6b199b100')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b6ccb50b193b93')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'], 'cb4cccb195b95')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'b6cccccb93b93')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'b299ccb99')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'ffccb197b50')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'ccccccccb197ccb197')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'b6cccccccccccccb293b193')

    def test_redundant_bet_raise(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b99b197')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b6ccb93b193')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'], 'cb4ccccb95b195')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'b6ccccccb93b193')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'cccb99cb199cb299')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'fb6fcb93b193')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'cfcccccb197cb297')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'cffcb10cb10b20cb67b267')

    def test_bet_amount(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b6b9')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b6cb12b24b30')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'], 'cb4cb4cb4b8b10')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'b6cccccb1')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'ccb98b99b100')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'ccccb2b4b6b8ccb9')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'ccccccccb96b97b98')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'ffccccccb50b55')

    def test_aggressor(self) -> None:
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6b99c', False), 0)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b99c', False), 1)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cccccccc', False), 0)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cccccb6ccc', False), 0)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cccccccb6b12c', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b299ccc', False), 2)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'ffb99c', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'cccccccccccccccc', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'ccccccccb2ccccccc', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'ccccccccccccb6b12b297ccc', False), 2)
        self.assert_actor(self.parse([100] * 4, ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b99ccc', False), 0)

    def test_showdown(self) -> None:
        self.assert_mucks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6b199c'), [False, False])
        self.assert_mucks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b99c'), [True, False])
        self.assert_mucks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6ccccccc'), [False, False])
        self.assert_mucks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cccccccc'), [False, False])
        self.assert_mucks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b4cb6f'), [False, True])
        self.assert_mucks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b299ccc'), [False, False, False, True])
        self.assert_mucks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'fb6ccccccccccc'), [False, False, True, True])
        self.assert_mucks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'fb6ccccb10b20cfcccb50c'), [True, False, True, True])
        self.assert_mucks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b6cccccb10b20cb93ccccccccc'), [False, False, True, True])
        self.assert_mucks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b6cccccb10b20cb93cccb50ccccc'), [False, False, True, True])
        self.assert_mucks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                     ['AcAsKc', 'Qs', 'Qc'], 'cccb149ccccccccccccccccc'),
                          [False, False, True, True, True, True])
        self.assert_mucks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                     [], 'b50fffff'), [True, True, False, True, True, True])
        self.assert_mucks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'TsTh', 'JcTc'],
                                     ['AcAsKc', 'Qs', 'Qc'], 'b50b199ccccf'), [False, False, True, True, True, False])
        self.assert_mucks(self.parse([100] * 4, ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b99ccc'),
                          [False, False, True, True])

    def test_distribution(self) -> None:
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6b199c'), [100, 200])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b99c'), [100, 200])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6ccccccc'), [193, 107])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cccccccc'), [197, 103])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b4cb6f'), [205, 95])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'b299ccc'), [300, 400, 100, 0])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'fb6ccccccccccc'), [193, 115, 299, 193])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'fb6ccccb10b20cfcccb50c'), [123, 195, 299, 183])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'b6cccccb10b20cb93ccccccccc'), [100, 400, 200, 100])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'b6cccccb10b20cb93cccb50ccccc'), [200, 400, 150, 50])
        self.assert_stacks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                      ['AcAsKc', 'Qs', 'Qc'], 'cccb149ccccccccccccccccc'), [300, 600, 150, 50, 50, 0])
        self.assert_stacks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                      [], 'b50fffff'), [198, 97, 308, 199, 199, 149])
        self.assert_stacks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'TsTh', 'JcTc'],
                                      ['AcAsKc', 'Qs', 'Qc'], 'b50b199ccccf'), [150, 0, 249, 0, 0, 751])

    def test_short_stacks(self) -> None:
        self.assert_stacks(self.parse([0, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [0, 0])
        self.assert_stacks(self.parse([1, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [1, 0])
        self.assert_stacks(self.parse([0, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [0, 1])
        self.assert_stacks(self.parse([2, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [1, 2])
        self.assert_stacks(self.parse([50, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [49, 2])
        self.assert_stacks(self.parse([0, 0, 0, 0], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], ''),
                           [0, 0, 0, 0])
        self.assert_stacks(self.parse([1, 1, 5, 5], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b4c'),
                           [0, 4, 8, 0])

    def assert_actor(self, game: PokerGame, index: Optional[int]) -> None:
        if isinstance(game.actor, PokerPlayer):
            self.assertEqual(game.actor.index, index)
        else:
            self.assertIsNone(index)

    def assert_mucks(self, game: PokerGame, mucks: Sequence[bool]) -> None:
        self.assertSequenceEqual([player.is_mucked for player in game.players], mucks)

    def assert_stacks(self, game: PokerGame, stacks: Sequence[int]) -> None:
        self.assertSequenceEqual([player.stack for player in game.players], stacks)

    def parse(self, stacks: Sequence[int], hole_card_sets: Sequence[str], board_card_sets: Sequence[str], tokens: str,
              terminate: bool = True) -> NLTHEGame:
        game = NLTHEGame(self.ANTE, self.BLINDS, stacks)

        for player, hole_cards in zip(game.players, hole_card_sets):
            game.nature.deal_player(player, *self.split_cards(hole_cards))

        try:
            while tokens or board_card_sets:
                if isinstance(game.actor, PokerPlayer):
                    token, tokens = tokens[0], tokens[1:]

                    if token == 'b':
                        if tokens.isdigit():
                            index = len(tokens)
                        else:
                            index = next(i for i, c in enumerate(tokens) if not c.isdigit())

                        amount, tokens = int(tokens[:index]), tokens[index:]
                        game.actor.bet_raise(amount)
                    elif token == 'c':
                        game.actor.check_call()
                    elif token == 'f':
                        game.actor.fold()
                    else:
                        self.fail()
                else:
                    game.nature.deal_board(*self.split_cards(board_card_sets[0]))
                    board_card_sets = board_card_sets[1:]
        except ActionException as exception:
            assert not tokens and not board_card_sets, 'DEBUG: An exception was raised before all commands were parsed'
            raise exception

        while terminate and not game.is_terminal and isinstance(game._stage, ShowdownStage):
            cast(PokerPlayer, game.actor).showdown()

        return game

    @staticmethod
    def split_cards(cards: str) -> Sequence[str]:
        return list(cards[i:i + 2] for i in range(0, len(cards), 2))


if __name__ == '__main__':
    main()
