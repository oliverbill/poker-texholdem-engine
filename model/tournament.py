import datetime
import random
from typing import List

from exception.noplayerisregistered_exception import NoPlayerRegisteredException
from model.blind import Blind
from model.player import Player
from model.player_rank import TournamentRank
from model.table import Table


class Tournament:
    def __init__(self, scheduled_start_datetime: datetime.datetime):
        self.__id = random.randint(1, 1000000)
        self.__scheduled_start_datetime = scheduled_start_datetime
        self.__initial_players: List[Player] = list()
        self.__left_players: List[Player] = list()
        self.__player_rank: List[TournamentRank] = list()
        self.__tables: List[Table] = list()
        self.__blinds = Blind.generate_blinds()

    def get_blinds(self):
        return self.__blinds
    def eliminate_player(self, player: Player):
        self.__left_players.remove(player)
    def register_player(self, player: Player):
        idx = len(self.__left_players)
        self.__left_players.insert(idx+1, player)
    def start(self):
        if self.is_at_start_time():
            self.__initial_players = self.__left_players
            if len(self.__initial_players and self.__left_players) == 0:
                raise NoPlayerRegisteredException('Please register players to this tournament')
            for i in range(len(self.__initial_players)):
                self.__player_rank.append(TournamentRank(i+1,  # para as posicoes do ranking comecarem com 1
                                          self.__initial_players[i]))

            self.create_tables_for_initial_players()

            self.seat_initial_players_in()
        else:
            print(f'wait until the tournament´s scheduled time: {self.__scheduled_start_datetime}')

    def create_tables_for_initial_players(self):
        table_qty_by_players_qty = int(len(self.__initial_players) / 9)
        if table_qty_by_players_qty < 9:
            table_qty_by_players_qty = 1
        for i in range(table_qty_by_players_qty):
            self.__tables.append(Table())

    def seat_initial_players_in(self):
        for p in self.__initial_players:
            create_new_table = False
            for t in self.__tables:
                next_vacant_seat = t.get_next_vacant_seat()
                if next_vacant_seat is not None:
                    next_vacant_seat.seat_in(p)
                else:
                    create_new_table = True
            if create_new_table:
                new_table = Table()
                self.__tables.append(new_table)
                new_table.get_next_vacant_seat().seat_in(p)

    def is_at_start_time(self):
        print(f'now={datetime.datetime.now()},start={self.__scheduled_start_datetime}')
        return datetime.datetime.now().minute == self.__scheduled_start_datetime.minute \
            and datetime.datetime.now().hour == self.__scheduled_start_datetime.hour

    def get_tables(self):
        return self.__tables

    def get_rank(self):
        return self.__player_rank

    def __str__(self):
        left_players_str = '|'.join(map(str, self.__left_players))
        player_rank_str = '|'.join(map(str, self.__player_rank))
        tables_str = '|'.join(map(str, self.__tables))
        blinds_str = '|'.join(map(str, self.__blinds))
        return \
            f'Tournament(id={self.__id}, start={self.__scheduled_start_datetime},' \
            f'left_players={left_players_str}, rank={player_rank_str}, ' \
            f'tables={tables_str},blinds={blinds_str})'
