from dto.communityhand_dto import CommunityHandDto
from exception.communityhandwithLessthanfivecards_exception import CommunityHandWithLessThanFiveCardsException
from model.card import Card
from model.player import Player

class ShowdownCardsDto:
    def __init__(self, community_hand: CommunityHandDto):
        if len(community_hand.hand_cards) != 5:
            raise CommunityHandWithLessThanFiveCardsException()
        hand_cards = community_hand.hand_cards
        # cards of the hand
        self.card1: Card = hand_cards[0]
        self.card2: Card = hand_cards[1]
        self.card3: Card = hand_cards[2]
        self.card4: Card = hand_cards[3]
        self.card5: Card = hand_cards[4]
        self.player: Player = community_hand.player
    def __str__(self):
        return f'ShowdownCardsDto(player={self.player}, card1={self.card1}, card2={self.card2}, ' \
               f'card3={self.card3}, card4={self.card4}, card5={self.card5})'
