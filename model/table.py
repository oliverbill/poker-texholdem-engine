import random
from typing import List

from exception.tableisfull_exception import TableIsFullException
from model.card_deck import CardDeck
from model.player import Player
from model.seat import Seat
from model.table_positions_enum import TablePositionsEnum


class Table:
    def __init__(self):  # cria um assento VAGO p cada posicao
        self.__id = random.randint(1, 1000000)
        self.__seats: List[Seat] = list()
        self.set_seats_positions()
        self.__card_deck = CardDeck()
    def get_next_vacant_seat(self) -> Seat:
        ## self.__seats.sort(key=lambda s: s.get_position_number()) # sort by position number
        for s in self.__seats:
            if not s.is_occupied():
                return s
    def seat_in(self, player: Player):
        vacant_seat = self.get_next_vacant_seat()
        if vacant_seat is None:
            raise TableIsFullException()
        vacant_seat.seat_in(player)

    def seat_out(self, player: Player):
        seat = self.is_player_seated(player)
        if seat is not None:
            seat.seat_out()

    def is_player_seated(self, player: Player) -> Seat:
        for s in self.__seats:
            if s.get_player() == player:
                return s
        return None

    def get_seats(self) -> List[Seat]:
        return self.__seats

    def get_active_seats(self) -> List[Seat]:
        active_seats: List[Seat] = list()
        for s in self.__seats:
            if s.is_occupied() and not s.is_seated_out():
                active_seats.append(s)
        return active_seats
    def get_card_deck(self) -> CardDeck:
        return self.__card_deck
    def set_seats_positions(self):
        names = [member.name for member in TablePositionsEnum]
        for name in names:
            self.__seats.append(Seat(name))

    def get_seat_by_position(self, position: TablePositionsEnum):
        return [seat for seat in self.get_seats() if seat.get_position_name == position]

    def __str__(self):
        seats_str = '|'.join(map(str, self.__seats))
        return \
            f'Table(id={self.__id}, seats={seats_str})'
