from gameservice.tictactoe.game import TicTacToeGame
from test import interactive_test, random_test


class CustomTTT(TicTacToeGame):
    labels = ["A", "B"]


a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(CustomTTT())
else:
    random_test(CustomTTT(), 1000000, 1000)
