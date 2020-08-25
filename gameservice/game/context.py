class Context:
    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        return self.__game

    @property
    def info(self):
        return {}
