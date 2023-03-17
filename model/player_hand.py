from model.card import Card


class PlayerHand:
    def __init__(self, card1: Card, card2: Card):
        self.__card1 = card1
        self.__card2 = card2
    def set_card_1(self, card: Card):
        if self.__card1 is not None:
            print(f'card 1 already set: {self.__card1}')
        else:
            self.__card1 = card
    def set_card_2(self, card: Card):
        if self.__card2 is not None:
            print(f'card 2 already set: {self.__card1}')
        else:
            self.__card2 = card
    def get_card1(self) -> Card:
        if self.__card1 is not None:
            return self.__card1
    def get_card2(self) -> Card:
        if self.__card2 is not None:
            return self.__card2
    def __str__(self):
        return f'PlayerHand(card1={self.__card1}, card2={self.__card2})'
