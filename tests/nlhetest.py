from gameservice.nlhe.game import NLHEGame
from test import interactive_test, random_test, print_infoset


class CustomNLHE(NLHEGame):
    blinds = [1, 2]
    starting_stacks = [200, 200, 300]

    def bet_sizes(self, min_raise, max_raise):
        amounts = set()

        while min_raise < max_raise:
            amounts.add(int(min_raise))
            min_raise *= 1.5

        amounts.add(max_raise)

        return sorted(amounts)


game = CustomNLHE()

a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(game)
else:
    random_test(game, 1000000, 1000)
