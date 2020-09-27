from gameservice.nlhe.game import NLHEGame
from test import interactive_test, random_test, print_infoset


class CustomNLHE(NLHEGame):
    blinds = [1, 2]
    starting_stacks = [200, 1000, 500, 1500, 600, 600]
    labels = list(range(len(starting_stacks)))

    def bet_sizes(self, min_raise, max_raise):
        amounts = set()

        while min_raise < max_raise:
            amounts.add(int(min_raise))
            min_raise *= 1.5

        amounts.add(max_raise)

        return sorted(amounts)


a = int(input("0: interactive\n1: random\nChoice: "))

if a == 0:
    interactive_test(CustomNLHE)
else:
    from threading import Thread

    threads = []

    for i in range(50):
        threads.append(Thread(target=random_test, args=(CustomNLHE, 100, 10)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
