from gameservice.tictactoe.game import TicTacToeGame
from test import interactive_test, random_test

a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(TicTacToeGame())
else:
    random_test(TicTacToeGame(), 1000000, 1000)
