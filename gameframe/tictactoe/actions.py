from gameframe.sequential import SequentialAction


class MarkAction(SequentialAction):
    """MarkAction is the class for mark actions."""

    def __init__(self, player, r, c):
        super().__init__(player)

        self.__r = r
        self.__c = c

    def __str__(self):
        return f'Mark row {self.r} column {self.c}'

    @property
    def r(self):
        """
        :return: the row number of this mark action
        """
        return self.__r

    @property
    def c(self):
        """
        :return: the column number of this mark action
        """
        return self.__c

    @property
    def is_applicable(self):
        return super().is_applicable and not self.actor.is_nature and 0 <= self.r < 3 and 0 <= self.c < 3 and \
               self.game.environment.board[self.r][self.c] is None

    @property
    def is_public(self):
        return True

    def act(self):
        super().act()

        self.game.environment.board[self.r][self.c] = self.actor

        if self.game.environment.empty_coordinates and self.game.environment.winner is None:
            self.game.actor = next(self.actor)
        else:
            self.game.actor = None
