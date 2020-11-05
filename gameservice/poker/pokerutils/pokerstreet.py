class PokerStreet:
    def __init__(self, num_hole_cards, num_board_cards):
        self.__num_hole_cards = num_hole_cards
        self.__num_board_cards = num_board_cards

    @property
    def num_hole_cards(self):
        return self.__num_hole_cards

    @property
    def num_board_cards(self):
        return self.__num_board_cards
