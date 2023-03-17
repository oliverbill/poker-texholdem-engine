from typing import List

from dto.showdown_result_dto import ShowdownResultDto
from model.action import ActionEnum
from model.flop import Flop
from model.player import Player
from model.player_action import PlayerAction
from model.player_hand import PlayerHand
from model.river import River
from model.seat import Seat
from model.table import Table
from model.table_hand import TableHand, HandStatus
from model.tournament import Tournament
from model.turn import Turn
from util.showdown_calculator import calculate_community_hands


# nao lancar excecao por uma questao de UX
# class ValueOfRaiseException(Exception):
#     def __init__(self, raise_value: int, last_bet: int):
#         super().__init__("raise value {} is not min double of last bet: {}".format(raise_value,last_bet))

class TableHandController:
    def __init__(self, table: Table, tournament: Tournament):
        # self.mq = RabbitMQConnector('')
        self.__hand = TableHand(table)
        self.__tournament = tournament
        self.__folded_hands: List[PlayerHand] = list()
        self.__last_bet = 0
    def preflop(self, player_actions: List[PlayerAction]):
        self.__hand.status = HandStatus.PRE_FLOP_STARTED

        level_one_blinds = self.__tournament.get_blinds()[1]
        self.__hand.pot = level_one_blinds.small_blind() \
                            + level_one_blinds.big_blind() \
                            + level_one_blinds.ante()

        self.__hand.deal(self.__hand.get_table().get_active_seats())

        # actions must be ordered by caller
        # player_actions.sort(key=lambda a: a.get_seat().get_position_number())
        for action in player_actions:
            self.process_player_action(action)

        self.__hand.status = HandStatus.PRE_FLOP_ENDED
    def process_player_action(self, action: PlayerAction):
        seat_action = action.get_action()
        if seat_action == ActionEnum.FOLD:
            hand = action.get_hand()
            self.__folded_hands.append(hand)
        if seat_action == ActionEnum.BET:
            self.__hand.pot += action.get_value()
            action.get_player().decrease_stack(action.get_value())
            self.__last_bet = action.get_value()
        if seat_action == ActionEnum.CALL:
            self.__hand.pot += action.get_value()
            action.get_player().decrease_stack(action.get_value())
            self.__last_bet = action.get_value()
        if seat_action == ActionEnum.RAISE:
            if action.get_value() < (self.__last_bet * 2):
                self.__hand.pot += self.__last_bet * 2
                value = self.__last_bet * 2
            else:
                self.__hand.pot += action.get_value()
                value = action.get_value()
            action.get_player().decrease_stack(value)
        self.__last_bet = action.get_value()
    def flop(self, player_actions: List[PlayerAction]) -> Flop:
        self.__hand.status = HandStatus.FLOP_STARTED
        deck = self.get_table_hand().get_table().get_card_deck()
        flop = Flop(deck.deal_card(), deck.deal_card(), deck.deal_card(), deck.deal_card())
        self.__hand.set_flop(flop)
        for action in player_actions:
            self.process_player_action(action)
        self.__hand.status = HandStatus.FLOP_ENDED
        return flop

    # def format_msg_player_action(self, msg_consumed: str) -> PlayerAction:
    #     json.load()
    def turn(self, player_actions: List[PlayerAction]) -> Turn:
        self.__hand.status = HandStatus.TURN_STARTED
        deck = self.get_table_hand().get_table().get_card_deck()
        turn = Turn(deck.deal_card(), deck.deal_card())
        self.__hand.set_turn(turn)
        for action in player_actions:
            self.process_player_action(action)
        self.__hand.status = HandStatus.TURN_ENDED
        return turn
    def river(self, player_actions: List[PlayerAction]) -> River:
        self.__hand.status = HandStatus.RIVER_STARTED
        deck = self.get_table_hand().get_table().get_card_deck()
        river = River(deck.deal_card(), deck.deal_card())
        self.__hand.set_river(river)
        for action in player_actions:
            self.process_player_action(action)
        self.__hand.status = HandStatus.RIVER_ENDED
        return river
    def showdown(self, active_seats: List[Seat], folded_hands: List[PlayerHand], table_hand: TableHand) \
            -> ShowdownResultDto:

        self.__hand.status = HandStatus.SHOWDOWN_STARTED
        showdown_dto = calculate_community_hands(active_seats, folded_hands, table_hand)
        for dto in showdown_dto.winner_hands:
            dto.player.increase_stack(self.get_table_hand().pot)
        self.get_table_hand().pot = 0
        self.get_table_hand().get_side_pots().clear()
        self.__hand.status = HandStatus.SHOWDOWN_ENDED
        return showdown_dto
    def eliminate_player(self, player: Player):
        self.__hand.get_table().seat_out(player)
        self.__tournament.eliminate_player(player)
    def get_table_hand(self):
        return self.__hand
    def get_tournament(self):
        return self.__tournament
    def get_folded_hands(self):
        return self.__folded_hands
