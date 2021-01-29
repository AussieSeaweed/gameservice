class HoldEmGame(PokerGame, ABC):
    """HoldEmGame is the abstract base class for all hold'em games."""

    def __init__(self, deck, evaluator, hole_card_count, board_card_counts, limit, ante, blinds, starting_stacks,
                 laziness=False):
        super().__init__(
            deck, evaluator, [BettingRound(self, 0, [False] * hole_card_count)] + list(map(
                lambda board_card_count: BettingRound(self, board_card_count, []), board_card_counts,
            )), limit, ante, blinds, starting_stacks, laziness,
        )


class TexasHoldEmGame(HoldEmGame, ABC):
    """TexasHoldEmGame is the abstract base class for all texas hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, laziness=False):
        super().__init__(StandardDeck(), StandardEvaluator(), 2, [3, 1, 1], limit, ante, blinds, starting_stacks,
                         laziness)


class NoLimitTexasHoldEmGame(TexasHoldEmGame, ABC):
    """NoLimitTexasHoldEmGame is the abstract base class for all no-limit texas hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, laziness=False):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, laziness)


class GreekHoldEmGame(HoldEmGame, ABC):
    """GreekHoldEmGame is the abstract base class for all greek hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, laziness=False):
        super().__init__(StandardDeck(), GreekHoldEmEvaluator(), 2, [3, 1, 1], limit, ante, blinds, starting_stacks,
                         laziness)


class NoLimitGreekHoldEmGame(GreekHoldEmGame, ABC):
    """NoLimitGreekHoldEmGame is the abstract base class for all no-limit greek hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, laziness=False):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, laziness)


class OmahaHoldEmGame(HoldEmGame, ABC):
    """OmahaHoldEmGame is the abstract base class for all omaha hold'em games."""

    def __init__(self, limit, ante, blinds, starting_stacks, laziness=False):
        super().__init__(StandardDeck(), OmahaHoldEmEvaluator(), 4, [3, 1, 1], limit, ante, blinds, starting_stacks,
                         laziness)


class NoLimitOmahaHoldEmGame(OmahaHoldEmGame, ABC):
    """NoLimitOmahaHoldEmGame is the abstract base class for all no-limit omaha hold'em games."""

    def __init__(self, ante, blinds, starting_stacks, laziness=False):
        super().__init__(NoLimit(self), ante, blinds, starting_stacks, laziness)
