import datetime
import unittest
from typing import List

from controller.table_hand_controller import TableHandController
from dto.communityhand_dto import CommunityHandDto
from model.action import ActionEnum
from model.card import Card
from model.flop import Flop
from model.player import Player
from model.player_action import PlayerAction
from model.player_hand import PlayerHand
from model.river import River
from model.table_hand import HandStatus
from model.table_positions_enum import TablePositionsEnum
from model.tournament import Tournament
from model.turn import Turn
from util.player_utils import get_player_seat
from util.showdown_calculator import rank_community_hands


class TestShowdown(unittest.TestCase):

    def setUp(self):

        self.tournament1 = Tournament(datetime.datetime.now())
        self.player1 = Player(50000, 1, 'billyalves')
        self.player2 = Player(50000, 2, 'abreuLisinho')
        self.player3 = Player(50000, 3, 'fidel')
        self.tournament1.register_player(self.player1)
        self.tournament1.register_player(self.player2)
        self.tournament1.register_player(self.player3)
        self.tournament1.start()

        big_blind = self.tournament1.get_blinds()[1].big_blind()
        bet_value = big_blind * 2.5
        three_times_bet_value = 3 * bet_value
        diff_raise_value_and_bet_value = three_times_bet_value - bet_value
        self.bet_action = PlayerAction(get_player_seat(self.tournament1, self.player1), ActionEnum.BET, bet_value)
        self.raise_action = PlayerAction(get_player_seat(self.tournament1, self.player2), ActionEnum.RAISE, three_times_bet_value)
        self.fold_action = PlayerAction(get_player_seat(self.tournament1, self.player3), ActionEnum.FOLD, 0)
        self.call_action = PlayerAction(get_player_seat(self.tournament1, self.player1), ActionEnum.CALL, diff_raise_value_and_bet_value)
        self.player_actions = [self.fold_action, self.bet_action, self.raise_action, self.call_action]

        self.controller = TableHandController(self.tournament1.get_tables()[0], self.tournament1)

        self.controller.get_table_hand().set_flop(Flop(Card('2c'),
                                                       Card('5h'),
                                                       Card('4h'),
                                                       Card('8h')))

        self.controller.get_table_hand().set_turn(Turn(Card('3c'), Card('3h')))
        self.controller.get_table_hand().set_river(River(Card('4c'), Card('2h')))
    def test_showdown(self):
        for s in self.controller.get_table_hand().get_table().get_seats():
            if s.get_position_name() == TablePositionsEnum.UTG.name: # billyalves
                s.set_player_hand(PlayerHand(Card('Jc'), Card('Ac')))
            if s.get_position_name() == TablePositionsEnum.UTG1.name: # abreuLisinho
                s.set_player_hand(PlayerHand(Card('3d'), Card('Qc')))
            if s.get_position_name() == TablePositionsEnum.MP.name: # fidel
                s.set_player_hand(PlayerHand(Card('Kc'), Card('5d')))

        stack_before = self.player1.get_stack()
        table_hand = self.controller.get_table_hand()
        folded_hands = [PlayerHand(Card('9c'), Card('5c'))]

        showdown_dto = self.controller.showdown(table_hand.get_table().get_active_seats(),
                                                folded_hands,
                                                table_hand)

        status = self.controller.get_table_hand().status

        self.assertEquals(status, HandStatus.SHOWDOWN_ENDED,
                          f'TableHand status is not {HandStatus.SHOWDOWN_ENDED}: {status}')

        for dto in showdown_dto.winner_hands:
            if dto.player.__eq__(self.player1):
                self.assertTrue(dto.player.get_stack() > stack_before)

        self.assertTrue(len(self.controller.get_table_hand().get_side_pots()) == 0)
        self.assertTrue(self.controller.get_table_hand().get_pot() == 0)
    def test_community_hands(self):
        community_hand1 = [Card('4h'), Card('5h'), Card('8h'),
                           Card('Jc'), Card('Ac')]
        community_hand2 = [Card('3d'), Card('4h'), Card('5h'),
                           Card('8h'), Card('Qc')]
        community_hand3 = [Card('4h'), Card('8h'), Card('Kc'),
                           Card('5h'), Card('5d')]

        dto1 = CommunityHandDto(self.player1, community_hand1)
        dto2 = CommunityHandDto(self.player2, community_hand2)
        dto3 = CommunityHandDto(self.player3, community_hand3)
        community_hands = [dto1, dto2, dto3]
        # board: 5h4h8h3h2h
        # JcAc
        # 3dQc
        # Kc5d
        # Tc6c
        card_values_sum_by_hand = rank_community_hands(community_hands)

        best_hand: CommunityHandDto = list(card_values_sum_by_hand.values())[-1]

        self.assertTrue(dto1 in list(card_values_sum_by_hand.values()))
        self.assertEquals(dto1.hand_cards, community_hand1)
        self.assertTrue(dto2 in list(card_values_sum_by_hand.values()))
        self.assertEquals(dto2.hand_cards, community_hand2)
        self.assertTrue(dto3 in list(card_values_sum_by_hand.values()))
        self.assertEquals(dto3.hand_cards, community_hand3)

        # best hand: 5h5dKc8h4h
        self.assertEquals(best_hand.hand_cards, community_hand3)
