import pickle
from gameservice.tictactoe.game import TicTacToeGame


class Game(TicTacToeGame):
    labels = [1, 2]


pickle.dump(Game(), open("ttt.gs", "wb"))

game = pickle.load(open("ttt.gs", "rb"))

print(game)
print(game.player)

game = pickle.loads(pickle.dumps(game))

print(game)
print(game.player)
