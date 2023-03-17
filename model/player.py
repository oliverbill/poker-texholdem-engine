import random

from model.player_hand import PlayerHand


class Player:
    def __init__(self, stack: int, player_id: int, nick: str) -> object:
        if player_id is not None:
            self.__id = player_id
        else:
            self.__id = random.randint(1, 1000000)
        self.__stack = stack
        self.__nick = nick
        self.__player_hand = None
    def get_stack(self):
        return self.__stack
    def increase_stack(self, value: int):
        self.__stack += value
    def decrease_stack(self, value: int):
        self.__stack -= value
    def set_player_hand(self, hand: PlayerHand):
        self.__player_hand = hand
    def get_player_hand(self):
        return self.__player_hand
    def __str__(self):
        return f'Player(id={self.__id}, stack={self.__stack},' \
               f'nick={self.__nick}, player_hand={self.__player_hand})'

    def __members(self):
        return self.__id, self.__player_hand, self.__stack, self.__nick
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False
    def __hash__(self):
        return hash((self.__id, self.__stack))
