class Environment:
    """Environment is the base class for all environments."""

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """
        :return: the game of the environment
        """
        return self.__game

    @property
    def _information(self):
        return {}
