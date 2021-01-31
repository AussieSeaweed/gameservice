from gameframe.tictactoe.bases import TTTAction, TTTGame, TTTPlayer


class MarkAction(TTTAction[TTTPlayer]):
    """MarkAction is the class for mark actions."""

    def __init__(self, game: TTTGame, actor: TTTPlayer, r: int, c: int):
        super().__init__(game, actor)

        self.__r = r
        self.__c = c

    def __str__(self) -> str:
        return f'Mark ({self.__r}, {self.__c})'

    @property
    def is_applicable(self) -> bool:
        return super().is_applicable and isinstance(self.game.env.actor, TTTPlayer) \
               and 0 <= self.__r < 3 and 0 <= self.__c < 3 and self.game.env.board[self.__r][self.__c] is None

    def act(self) -> None:
        super().act()

        self.game.env._board[self.__r][self.__c] = self.actor

        if self.game.env.empty_coords and self.game.env.winner is None:
            self.game.env._actor = next(self.actor)
        else:
            self.game.env._actor = None
