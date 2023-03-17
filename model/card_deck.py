import queue
from random import shuffle

from errors import EmptyCardDeckException
from model.card import Card

# one for each Table
class CardDeck:
    def __init__(self):
        self.__cards = queue.LifoQueue().queue
        self.fill_up()
    def fill_up(self):
        self.__cards.clear()
        for card in Card.get_all_cards():
            self.__cards.append(Card(card))
    def shuffle(self):
        self.fill_up()
        shuffle(self.__cards)
    def deal_card(self) -> Card:
        if self.is_empty():
            raise EmptyCardDeckException()
        return self.__cards.pop()
    def is_empty(self):
        return len(self.__cards) == 0
    def card_qtty(self):
        return len(self.__cards)
