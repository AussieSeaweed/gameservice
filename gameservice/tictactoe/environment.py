from ..game import Environment


class TTTEnvironment(Environment):
    def __init__(self):
        super().__init__()

        self.__board = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]
