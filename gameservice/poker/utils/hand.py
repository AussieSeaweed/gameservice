class Hand:
    def __init__(self, hand_rank):
        self.__hand_rank = hand_rank

    def __lt__(self, other):
        return self.__hand_rank < other.__hand_rank

    def __eq__(self, other):
        return self.__hand_rank == other.__hand_rank

    def __hash__(self):
        return hash(self.__hand_rank)
