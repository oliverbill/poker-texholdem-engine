from model.card import Card


class Flop:
    def __init__(self, discard: Card, card1: Card, card2: Card, card3: Card):
        self.__discard = discard
        self.__card1 = card1
        self.__card2 = card2
        self.__card3 = card3
    
    def get_card1(self):
        return self.__card1
    def get_card2(self):
        return self.__card2
    def get_card3(self):
        return self.__card3
    def get_discard(self):
        return self.__discard
    def get_board(self):
        return self.__card1.get_suit() + self.__card2.get_suit() + self.get_card3().get_suit()
    def __str__(self):
        return f'Flop(board={self.get_board()}, discard={self.__discard}, card1={self.__card1}, card2={self.__card2}, card3={self.__card3})'
