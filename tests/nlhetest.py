from gameservice.nlhe.game import NLHEGame
from test import interactive_test, random_test


class CustomNLHE(NLHEGame):
    ante = 1
    blinds = [1, 2]
    starting_stacks = [200, 300, 300, 1000, 400, 500, 300, 200, 200]

    labels = list(map(str, range(len(starting_stacks))))


a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(CustomNLHE)
else:
    random_test(CustomNLHE, 1000, 100)
