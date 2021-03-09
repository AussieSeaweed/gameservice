"""This is a sample tic tac toe game resulting in the first player winning."""
from gameframe.ttt import TTTGame, parse_ttt

game = TTTGame()

parse_ttt(game, (
    (0, 0),
    (1, 0),
    (0, 1),
    (1, 1),
    (0, 2),
))

print('Board:')
print('\n'.join(map(lambda row: ' '.join(map(str, row)), game.board)))
print(f'Winner: {game.winner}')
