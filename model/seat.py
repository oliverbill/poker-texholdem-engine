from model.player import Player
from model.player_hand import PlayerHand
from model.table_positions_enum import TablePositionsEnum


class Seat:
    def __init__(self, position_name: str):
        self.__number = TablePositionsEnum[position_name].value
        self.__name = position_name
        self.__occupied = False
        self.__player: Player = None
        self.__seated_out = False
        self.__player_hand = None
    def seat_in(self, player: Player):
        self.__player = player
        self.__occupied = True
    def seat_out(self):
        self.__seated_out = True
    def is_occupied(self) -> bool:
        return self.__occupied
    def is_seated_out(self) -> bool:
        return self.__seated_out
    def set_player_hand(self, hand: PlayerHand):
        self.__player_hand = hand
    def get_position_name(self) -> str:
        return str(self.__name)
    def get_position_number(self) -> int:
        return self.__number
    def get_player(self) -> Player:
        return self.__player
    def get_hand(self) -> PlayerHand:
        return self.__player_hand

    def __str__(self):
        return f'Seat(number={self.__number}, name={self.__name}, occupied={self.__occupied}, ' \
               f'player={self.__player}, __seated_out={self.__seated_out}, player_hand={self.__player_hand})'
