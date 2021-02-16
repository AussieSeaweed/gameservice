from unittest import TestCase, main

from gameframe.poker import NLOGame, NLTGame, parse_poker_game


class ParserTestCase(TestCase):
    def test_nlt(self) -> None:
        game = NLTGame(500, [1000, 2000], [1125600, 2000000, 553500])

        parse_poker_game(
            game,
            'dp 0 Ac2d',
            'dp 1 5h7s',
            'dp 2 7h6h',
            'br 7000',
            'br 23000',
            'f',
            'cc',
            'db Jc3d5c',
            'br 35000',
            'cc',
            'db 4h',
            'br 90000',
            'br 232600',
            'br 1067100',
            'cc',
            'db Jh',
        )

        self.assertEqual(game.pot, 1109500)

        parse_poker_game(
            game,
            's',
            's',
        )

        self.assertSequenceEqual([player.bet for player in game.players], [0, 0, 0])
        self.assertSequenceEqual([player.stack for player in game.players], [572100, 1997500, 1109500])
        self.assertSequenceEqual([player.shown for player in game.players], [True, False, True])
        self.assertSequenceEqual([player.mucked for player in game.players], [False, True, False])

    def test_nlo(self) -> None:
        game = NLOGame(0, [50000, 100000], [125945025, 67847350])

        parse_poker_game(
            game,
            'dp 0 Ah3sKsKh',
            'dp 1 6d9s7d8h',
            'br 300000',
            'br 900000',
            'br 2700000',
            'br 8100000',
            'cc',
            'db 4s5c2h',
            'br 9100000',
            'br 43500000',
            'br 77900000',
            'cc',
            'db 5h',
            'db 9c',
        )

        self.assertEqual(game.pot, 135694700)

        parse_poker_game(
            game,
            's',
            's',
        )

        self.assertSequenceEqual([player.bet for player in game.players], [0, 0])
        self.assertSequenceEqual([player.stack for player in game.players], [193792375, 0])
        self.assertSequenceEqual([player.shown for player in game.players], [True, False])
        self.assertSequenceEqual([player.mucked for player in game.players], [False, True])


if __name__ == '__main__':
    main()
