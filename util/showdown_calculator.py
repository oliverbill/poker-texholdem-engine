from typing import List

from dto.communityhand_dto import CommunityHandDto
from dto.showdown_result_dto import ShowdownResultDto
from dto.showdowncards_dto import ShowdownCardsDto
from model.card import Card
from model.player_hand import PlayerHand
from model.seat import Seat
from model.table_hand import TableHand


def calculate_community_hands(active_seats: List[Seat],
                              folded_hands: List[PlayerHand],
                              table_hand: TableHand) -> ShowdownResultDto:

    community_hands_dto_list: List[CommunityHandDto] = list()
    winner_hands: List[ShowdownCardsDto] = list()
    loser_hands: List[ShowdownCardsDto] = list()
    for seat in active_seats:
        if seat.get_hand() not in folded_hands:
            community_hands_dto_list.append(assemble_community_hand(seat, table_hand))
    card_values_sum_by_hand = rank_community_hands(community_hands_dto_list)
    result = extract_winner_loser_hands(card_values_sum_by_hand, loser_hands, winner_hands)
    return result
def assemble_community_hand(seat: Seat, hand: TableHand) -> CommunityHandDto:
    if hand is None:
        raise ValueError('table hand is None')
    community_hand: List[Card] = list()
    community_hand.append(seat.get_hand().get_card1())
    community_hand.append(seat.get_hand().get_card2())
    community_hand.append(hand.get_card1())
    community_hand.append(hand.get_card2())
    community_hand.append(hand.get_card3())
    community_hand.append(hand.get_card4())
    community_hand.append(hand.get_card5())

    def sort_by_card_key(e: Card):
        return e.get_number()

    community_hand.sort(key=sort_by_card_key)

    print(f'low card removed:{community_hand.pop(0)}')
    print(f'low card removed:{community_hand.pop(0)}')
    to_str = '|'.join(map(str, community_hand))
    print(f'sorted hand: {to_str}')
    community_hand_dto = CommunityHandDto(seat.get_player(), community_hand)

    return community_hand_dto
def extract_winner_loser_hands(card_values_sum_by_hand, loser_hands, winner_hands) -> ShowdownResultDto:
    # appends only the best hand (for now)
    best_hand = list(card_values_sum_by_hand.values())[-1]
    winner_hands.append(ShowdownCardsDto(best_hand))
    # appends the rest of the hands as loser hands
    lista = list(card_values_sum_by_hand.values())
    for i in lista[1:]:
        loser_hands.append(ShowdownCardsDto(i))
    return ShowdownResultDto(winner_hands, loser_hands)
def rank_community_hands(community_hands_dto_list: List[CommunityHandDto]):
    if len(community_hands_dto_list) == 0:
        raise ValueError('community_hands_dto_list is empty')
    card_values_sum_by_hand = dict()
    cards_values_sum = 0
    for dto in community_hands_dto_list:
        for card in dto.hand_cards:
            cards_values_sum += card.get_number()  # sum all cards values of the hand
        card_values_sum_by_hand[cards_values_sum] = dto
    sorted(card_values_sum_by_hand.items())  # sort hands by sum value
    return card_values_sum_by_hand
