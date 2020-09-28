from gameservice.nlhe.game import NLHEGame
from test import interactive_test, random_test


class CustomNLHE(NLHEGame):
    blinds = [1, 2]
    starting_stacks = [200, 1000, 500, 1500, 600, 600, 2000]
    labels = list(range(len(starting_stacks)))

    # def bet_sizes(self, min_raise, max_raise):
    #     amounts = set()
    #
    #     while min_raise < max_raise:
    #         amounts.add(int(min_raise))
    #         min_raise *= 1.5
    #
    #     amounts.add(max_raise)
    #
    #     return sorted(amounts)

    def bet_sizes(self, min_raise, max_raise):
        return [max_raise]


a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(CustomNLHE)
else:
    random_test(CustomNLHE, 1000, 100)
