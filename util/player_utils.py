from typing import List

from model.action import ActionEnum
from model.player import Player
from model.player_action import PlayerAction
from model.seat import Seat
from model.tournament import Tournament


def get_player_seat(tournament: Tournament, player: Player) -> Seat:
    for table in tournament.get_tables():
        for seat in table.get_seats():
            if seat.get_player().__eq__(player):
                return seat
    raise AssertionError(f'Player {player} is not seated in any table')
def add_player_actions(tournament: Tournament, *players) -> List[PlayerAction]:

    big_blind = tournament.get_blinds()[1].big_blind()
    bet_value = big_blind * 2.5
    three_times_bet_value = 3 * bet_value
    diff_raise_value_and_bet_value = three_times_bet_value - bet_value
    bet_action = PlayerAction(get_player_seat(tournament, players[0]), ActionEnum.BET, bet_value)
    raise_action = PlayerAction(get_player_seat(tournament, players[1]), ActionEnum.RAISE, three_times_bet_value)
    fold_action = PlayerAction(get_player_seat(tournament, players[2]), ActionEnum.FOLD, 0)
    call_action = PlayerAction(get_player_seat(tournament, players[0]), ActionEnum.CALL, diff_raise_value_and_bet_value)

    player_actions = [fold_action, bet_action, raise_action, call_action]
    return player_actions
