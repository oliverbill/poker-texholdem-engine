import datetime
import random
from dataclasses import dataclass
from enum import Enum
from typing import List

from model.card import Card
from model.flop import Flop
from model.player_hand import PlayerHand
from model.river import River
from model.seat import Seat
from model.table import Table
from model.table_positions_enum import TablePositionsEnum
from model.turn import Turn


class HandStatus(Enum):
    NOT_DEALT = 'NOT_DEALT'
    PRE_FLOP_ENDED = 'PRE_FLOP_ENDED'
    PRE_FLOP_STARTED = 'PRE_FLOP_STARTED'
    FLOP_STARTED = 'FLOP_STARTED'
    FLOP_ENDED = 'FLOP_ENDED'
    TURN_STARTED = 'TURN_STARTED'
    TURN_ENDED = 'TURN_ENDED'
    RIVER_STARTED = 'RIVER_STARTED'
    RIVER_ENDED = 'RIVER_ENDED'
    SHOWDOWN_STARTED = 'SHOWDOWN_STARTED'
    SHOWDOWN_ENDED = 'SHOWDOWN_ENDED'
@dataclass
class TableHand:
    def __init__(self, table: Table):
        self.__id = random.randint(1, 1000000)
        self.__date_time = datetime.datetime.now()
        self.__table = table
        self.status = HandStatus.NOT_DEALT
        self.pot = 0
        self.__side_pots: [int] = list()
        self.__flop = None
        self.__turn = None
        self.__river = None
    def deal(self, seats: List[Seat]):
        for seat in seats:
            self.deal_card_1_to_seat(seat)
        for seat in seats:
            self.deal_card_2_to_seat(seat)
    def deal_card_1_to_seat(self, seat: Seat):
        print('dealing card1 to ' + seat.get_position_name())
        card = self.__table.get_card_deck().deal_card()
        hand_with_only_card1 = PlayerHand(card, None)
        seat.set_player_hand(hand_with_only_card1)
        seat.get_player().set_player_hand(hand_with_only_card1)
    def deal_card_2_to_seat(self, seat: Seat):
        print('dealing card2 to ' + seat.get_position_name())
        card2 = self.__table.get_card_deck().deal_card()
        seat.get_hand().set_card_2(card2)
        seat.get_player().get_player_hand().set_card_2(card2)
    def get_table(self) -> Table:
        return self.__table
    def set_flop(self, flop: Flop):
        self.__flop = flop
    def set_turn(self, turn: Turn):
        self.__turn = turn
    def set_river(self, river: River):
        self.__river = river
    def get_card1(self) -> Card:
        if self.__flop is not None:
            return self.__flop.get_card1()
    def get_card2(self) -> Card:
        if self.__flop is not None:
            return self.__flop.get_card2()
    def get_card3(self) -> Card:
        if self.__flop is not None:
            return self.__flop.get_card3()
    def get_card4(self) -> Card:
        if self.__turn is not None:
            return self.__turn.get_card()
    def get_card5(self) -> Card:
        if self.__river is not None:
            return self.__river.get_card()
    def get_pot(self) -> int:
        return self.pot
    def get_side_pots(self) -> List[int]:
        return self.__side_pots
    def get_board(self) -> str:
        c1 = ' ' + self.get_card1().get_suit()
        c2 = ' ' + self.get_card2().get_suit()
        c3 = ' ' + self.get_card3().get_suit()
        c4 = ' ' + self.get_card4().get_suit()
        c5 = ' ' + self.get_card5().get_suit()
        return c1 + c2 + c3 + c4 + c5
    def __str__(self):
        return f'TableHand(id={self.__id}, board={self.get_board()}, time={str(self.__date_time)},' \
               f' table={self.__table}, status={self.status},pot={self.pot}, side_pots={self.__side_pots}, ' \
               f' flop={self.__flop}, ' \
               f' turn={self.__turn},' \
               f' river={self.__river})'
