from model.card_enum import CardEnum
from model.suits_enum import SuitEnum


class Card:
    def __init__(self, value: str):
        self.__number = None
        self.__suit = None
        arg_card_number = value[0:1]
        arg_card_suit = value[1]
        card_values = [member.value for member in CardEnum]
        suit_values = [member.value for member in SuitEnum]
        if self.is_broadway(arg_card_number):
            arg_card_number = self.broadway_to_int(arg_card_number)
            self.full_card = self.int_to_broadway(arg_card_number) + arg_card_suit
        else:
            self.full_card = arg_card_number + arg_card_suit

        if (int(arg_card_number) not in card_values) or (arg_card_suit not in suit_values):
            raise ValueError(f'value not found: {value}')

        self.__number = int(arg_card_number)
        self.__suit = arg_card_suit
    def __str__(self):
        return f'Card({self.full_card}, number={self.__number}, suit={self.__suit})'
    @staticmethod
    def broadway_to_int(value: str) -> int:
        if value == 'T':
            return 10
        elif value == 'J':
            return 11
        elif value == 'Q':
            return 12
        elif value == 'K':
            return 13
        elif value == 'A':
            return 14
        else:
            return 0
    @staticmethod
    def int_to_broadway(value: int) -> str:
        if value == 10:
            return 'T'
        elif value == 11:
            return 'J'
        elif value == 12:
            return 'Q'
        elif value == 13:
            return 'K'
        elif value == 14:
            return 'A'
        else:
            return ' '
    @staticmethod
    def is_broadway(value: str):
        return value in ['T', 'J', 'Q', 'K', 'A']
    @classmethod
    def get_all_cards(cls):
        all_cards = []
        card_values = [member.value for member in CardEnum]
        suit_values = [member.value for member in SuitEnum]
        for card in card_values:
            for suit in suit_values:
                if card == 10:
                    all_cards.append('T' + suit)
                    continue
                if card == 11:
                    all_cards.append('J' + suit)
                    continue
                if card == 12:
                    all_cards.append('Q' + suit)
                    continue
                if card == 13:
                    all_cards.append('K' + suit)
                    continue
                if card == 14:
                    all_cards.append('A' + suit)
                    continue
                all_cards.append(str(card) + suit)
        return all_cards
    def get_number(self):
        return self.__number
    def get_suit(self):
        return self.__suit
    def __hash__(self):
        return hash(self.__number)
    def __eq__(self, other):
        if type(other) is type(self):
            return self.full_card == other.full_card
        else:
            return False
