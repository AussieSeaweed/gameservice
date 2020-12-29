from abc import ABC


class Round(ABC):
    """Round is the abstract base class for all rounds."""
    pass


class BettingRound(Round, ABC):
    """BettingRound is the abstract base class for all betting rounds."""
    pass


class LimitBettingRound(BettingRound):
    """LimitBettingRound is the class for limit betting rounds."""
    pass


class PotLimitBettingRound(BettingRound):
    """PotLimitBettingRound is the class for pot-limit betting rounds."""
    pass


class NoLimitBettingRound(BettingRound):
    """NoLimitBettingRound is the class for no-limit betting rounds."""
    pass


class DrawingRound(Round):
    """DrawingRound is the class for drawing rounds."""
    pass


class SetupRound(Round):
    """SetupRound is the class for setup rounds."""
    pass
