"""This is a sample tic tac toe game resulting in the first player winning."""
from gameframe.games.tictactoe import TicTacToeGame, parse_tic_tac_toe

game = TicTacToeGame()

parse_tic_tac_toe(game, (
    (0, 0),
    (1, 0),
    (0, 1),
    (1, 1),
    (0, 2),
))
