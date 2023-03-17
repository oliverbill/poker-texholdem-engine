import datetime
import unittest
from typing import List

from controller.table_hand_controller import TableHandController
from model.action import ActionEnum
from model.player import Player
from model.player_action import PlayerAction
from model.seat import Seat
from model.table_hand import HandStatus
from model.table_positions_enum import TablePositionsEnum
from model.tournament import Tournament
from util.player_utils import add_player_actions, get_player_seat


class TableHandTestCase(unittest.TestCase):
    def setUp(self):

        self.tournament1 = Tournament(datetime.datetime.now())
        self.player1 = Player(50000, 1, 'billyalves')
        self.player2 = Player(50000, 2, 'abreuLisinho')
        self.player3 = Player(50000, 3, 'fidel')
        self.tournament1.register_player(self.player1)
        self.tournament1.register_player(self.player2)
        self.tournament1.register_player(self.player3)
        self.tournament1.start()

        self.controller = TableHandController(self.tournament1.get_tables()[0], self.tournament1)

        self.player_actions = add_player_actions(self.tournament1, self.player1, self.player2, self.player3)

        big_blind = self.tournament1.get_blinds()[1].big_blind()
        bet_value = big_blind * 2.5
        three_times_bet_value = 3 * bet_value
        diff_raise_value_and_bet_value = three_times_bet_value - bet_value
        self.bet_action = PlayerAction(get_player_seat(self.tournament1, self.player1), ActionEnum.BET, bet_value)
        self.raise_action = PlayerAction(get_player_seat(self.tournament1, self.player2), ActionEnum.RAISE,
                                         three_times_bet_value)
        self.fold_action = PlayerAction(get_player_seat(self.tournament1, self.player3), ActionEnum.FOLD, 0)
        self.call_action = PlayerAction(get_player_seat(self.tournament1, self.player1), ActionEnum.CALL,
                                        diff_raise_value_and_bet_value)
        self.player_actions = [self.fold_action, self.bet_action, self.raise_action, self.call_action]

        self.assertTrue(len(self.tournament1.get_tables()) != 0,
                        f'No tables created for the tournament: {self.tournament1}')

        self.assert_table_positions_are_correct(self.tournament1)

        level_one_blinds = self.controller.get_tournament().get_blinds()[1]
        # pot = 25
        self.pot = level_one_blinds.small_blind() \
                          + level_one_blinds.big_blind() \
                          + level_one_blinds.ante()
    def test_rank_is_FILO_ordered(self):
        rank = self.tournament1.get_rank()[0]
        self.assertTrue(rank.player == self.player1, 'player 1 is not in the rank')
        self.assertTrue(rank.position == 1, 'player 1 is not in the position 1')
        rank = self.tournament1.get_rank()[1]
        self.assertTrue(rank.player == self.player2, 'player 2 is not in the rank')
        self.assertTrue(rank.position == 2, 'player 2 is not in the position 2')
        rank = self.tournament1.get_rank()[2]
        self.assertTrue(rank.player == self.player3, 'player 3 is not in the rank')
        self.assertTrue(rank.position == 3, 'player 3 is not in the position 3')
    def test_preflop(self):
        self.controller.preflop(self.player_actions)

        status = self.controller.get_table_hand().status
        self.assertEquals(status, HandStatus.PRE_FLOP_ENDED,
                          f'TableHand status is not {HandStatus.PRE_FLOP_ENDED}: {status}')

        pot = self.controller.get_table_hand().pot
        self.assertEquals(pot, 175, f'Pot is not $175: {pot}')

        self.assert_cards_dealt(self.controller.get_table_hand().get_table().get_seats())

        self.assertEquals(self.player_actions[0], self.fold_action, f'process_action_list not sorted by table position')
        self.assertEquals(self.player_actions[1], self.bet_action, f'process_action_list not sorted by table position')
        self.assertEquals(self.player_actions[2], self.raise_action, f'process_action_list not sorted by table position')
        self.assertEquals(self.player_actions[3], self.call_action, f'process_action_list not sorted by table position')
    def test_flop(self):
        flop = self.controller.flop(self.player_actions)

        status = self.controller.get_table_hand().status
        self.assertEquals(status, HandStatus.FLOP_ENDED,
                          f'TableHand status is not {HandStatus.FLOP_ENDED}: {status}')

        self.assertIsNotNone(flop.get_discard(), f'Flop discard not dealt')
        self.assertIsNotNone(flop.get_card1(), f'Flop card 1 not dealt')
        self.assertIsNotNone(flop.get_card2(), f'Flop card 2 not dealt')
        self.assertIsNotNone(flop.get_card3(), f'Flop card 3 not dealt')
    def test_turn(self):
        turn = self.controller.turn(self.player_actions)

        status = self.controller.get_table_hand().status
        self.assertEquals(status, HandStatus.TURN_ENDED,
                          f'TableHand status is not {HandStatus.TURN_ENDED}: {status}')

        self.assertIsNotNone(turn.get_discard(), f'Turn discard not dealt')
        self.assertIsNotNone(turn.get_card(), f'Turn card not dealt')
    def test_river(self):
        river = self.controller.river(self.player_actions)

        status = self.controller.get_table_hand().status
        self.assertEquals(status, HandStatus.RIVER_ENDED,
                          f'TableHand status is not {HandStatus.RIVER_ENDED}: {status}')

        self.assertIsNotNone(river.get_discard(), f'River discard not dealt')
        self.assertIsNotNone(river.get_card(), f'River card not dealt')
    def test_player_action_fold(self):
        self.controller.process_player_action(self.fold_action)
        self.assertTrue(self.fold_action.get_hand() in self.controller.get_folded_hands(),
                        f'fold action hand not saved in folded_hands')
    def test_player_action_bet(self):
        decreased_stack = self.bet_action.get_player().get_stack() - self.bet_action.get_value()
        # because we are not calling "pre_flop"
        self.controller.get_table_hand().pot += self.pot
        increased_pot = self.controller.get_table_hand().pot + self.bet_action.get_value()

        self.controller.process_player_action(self.bet_action)

        self.assertEquals(self.bet_action.get_player().get_stack(), decreased_stack)
        self.assertEquals(self.controller.get_table_hand().pot, increased_pot)
    def test_player_action_call(self):
        stack_decreased = self.call_action.get_player().get_stack() - self.call_action.get_value()
        # because we are not calling "pre_flop"
        self.controller.get_table_hand().pot += self.pot
        increased_pot = self.controller.get_table_hand().pot + self.call_action.get_value()

        self.controller.process_player_action(self.call_action)

        self.assertEquals(self.bet_action.get_player().get_stack(), stack_decreased)
        self.assertEquals(self.controller.get_table_hand().get_pot(), increased_pot)
    def test_player_action_raise(self):
        stack_decreased = self.raise_action.get_player().get_stack() - self.raise_action.get_value()
        # because we are not calling "pre_flop"
        self.controller.get_table_hand().pot += self.pot
        increased_pot = self.controller.get_table_hand().pot + self.raise_action.get_value()

        self.controller.process_player_action(self.raise_action)

        self.assertEquals(self.raise_action.get_player().get_stack(), stack_decreased)
        self.assertEquals(self.controller.get_table_hand().get_pot(), increased_pot)
    def assert_cards_dealt(self, seats: List[Seat]):
        hand = self.controller.get_table_hand()
        seats_with_hands_dealt = hand.deal(seats)
        self.assertIsNotNone(seats_with_hands_dealt, f'no hand dealt to seats')
        self.assertEquals(len(seats_with_hands_dealt), 9)
    def assert_table_positions_are_correct(self, tournament: Tournament):
        official_positions = [member.name for member in TablePositionsEnum]
        for table in tournament.get_tables():
            seats = table.get_seats()
            for i in range(len(seats)):
                seat = table.get_seats()[i]
                position = seat.get_position_name()
                self.assertTrue(position == official_positions[i],
                                f'Position in preflop must be {official_positions[i]}, not {position}')


if __name__ == '__main__':
    unittest.main()
