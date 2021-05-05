from abc import ABC
from typing import final


@final
class GameFrameValueError(ValueError, ABC):
    """GameFrameValueError is the base exception class for all GameFrame value errors."""
    ...
