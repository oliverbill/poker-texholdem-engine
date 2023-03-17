from model.card import Card


class River:
    def __init__(self, discard: Card, card: Card):
        self.__discard = discard
        self.__card = card
    def get_card(self):
        return self.__card
    def get_discard(self):
        return self.__discard
    def __str__(self):
        return f'River(discard={self.__discard}, card={self.__card})'