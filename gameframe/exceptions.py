class GameFrameError(Exception):
    """GameFrameError is the exception class for all GameFrame errors."""
    ...


class GameFrameValueError(GameFrameError, ValueError):
    """GameFrameValueError is the exception class for all GameFrame value errors."""
    ...
