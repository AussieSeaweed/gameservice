from gameservice.nlhe.game import NLHEGame
from test import interactive_test, random_test


class CustomNLHE(NLHEGame):
    ante = 2
    blinds = [5, 10]
    starting_stacks = [200, 400, 400, 1000, 800, 2000, 200]

    labels = list(map(str, range(len(starting_stacks))))


a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(CustomNLHE)
else:
    random_test(CustomNLHE, 1000, 100)
