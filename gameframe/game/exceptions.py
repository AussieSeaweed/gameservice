from typing import final


class GameFrameException(Exception):
    pass


@final
class TerminalityException(GameFrameException):
    pass


@final
class PlayerTypeException(GameFrameException):
    pass
