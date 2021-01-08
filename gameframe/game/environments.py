class Environment:
    """Environment is the base class for all environments.

    The environment contains global information about a game state that does not belong to any actor in particular and
    is public.
    """

    def __init__(self, game):
        self._game = game

    @property
    def _information(self):
        return {}
