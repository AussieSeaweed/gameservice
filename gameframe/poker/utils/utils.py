from enum import Enum, unique


@unique
class HoleCardStatus(Enum):
    """HoleCardStatus is the enum for hole card statuses."""
    DEFAULT = 0
    SHOWN = 1
    MUCKED = 2
