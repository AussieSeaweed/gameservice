from gameframe.poker import NoLimitTexasHoldEmGame
from gameframe.sequential.tests import interact_sequential

__all__ = ['interact_poker']


def interact_poker() -> None:
    """Interacts with a poker game."""
    interact_sequential(lambda: NoLimitTexasHoldEmGame(1, [1, 2], [50, 25], True))


if __name__ == '__main__':
    interact_poker()
