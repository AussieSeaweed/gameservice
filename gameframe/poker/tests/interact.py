from gameframe.sequential.tests import interact_sequential
from gameframe.poker import NoLimitTexasHoldEmGame


def main() -> None:
    """Interacts with a tic tac toe game."""
    interact_sequential(lambda: NoLimitTexasHoldEmGame(1, [1, 2], [50, 25], True))


if __name__ == '__main__':
    main()
