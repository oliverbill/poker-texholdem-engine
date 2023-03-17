from model.action import ActionEnum
from model.player import Player
from model.player_hand import PlayerHand
from model.seat import Seat

class PlayerAction:
    def __init__(self, seat: Seat, action: ActionEnum, value: int = 0):
        self.__seat = seat
        self.__player = seat.get_player()
        self.__hand = seat.get_hand()
        self.__action = action
        self.__value = value  # for CHECK and FOLD, value = 0
    def get_player(self) -> Player:
        return self.__player
    
    def get_action(self) -> ActionEnum:
        return self.__action
    
    def get_value(self) -> int:
        return self.__value
    
    def get_seat(self) -> Seat:
        return self.__seat
    
    def get_hand(self) -> PlayerHand:
        return self.__hand

    def __str__(self):
        return f'PlayerAction(seat={self.__seat}, player={self.__player}, hand={self.__hand}, action={self.__action}' \
            f', value={self.__value}'
