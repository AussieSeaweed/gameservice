from unittest import TestCase, main

from gameframe.tictactoe import TTTGame


class TTTSampleGameTestCase(TestCase):
    """TTTSampleGameTestCase is the class for sample tic tac toe test cases."""

    def test_draw(self) -> None:
        """Tests if tic tac toe properly detects a case of a tied game.

        :return: None
        :raise AssertionError: if the winner is wrongly detected
        """
        game = TTTGame()

        game.players[0].actions[4].act()

        while game.env.actor is not None:
            game.env.actor.actions[0].act()

        self.assertIsNone(game.env.winner)

    def test_loss(self) -> None:
        """Tests if tic tac toe properly detects a case of the first player
        losing.

        :return: None
        :raise AssertionError: if the winner is wrongly detected
        """
        game = TTTGame()

        game.players[0].actions[8].act()

        while game.env.actor is not None:
            game.env.actor.actions[0].act()

        self.assertEqual(game.players[1], game.env.winner)

    def test_win(self) -> None:
        """Tests if tic tac toe properly detects a case of the first player
        winning.

        :return: None
        :raise AssertionError: if the winner is wrongly detected
        """
        game = TTTGame()

        while game.env.actor is not None:
            game.env.actor.actions[0].act()

        self.assertEqual(game.players[0], game.env.winner)


if __name__ == '__main__':
    main()
