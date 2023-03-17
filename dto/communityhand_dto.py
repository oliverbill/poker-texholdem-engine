from typing import List

from model.card import Card
from model.player import Player
class CommunityHandDto:
    def __init__(self, player: Player, cards: List[Card]):
        self.player: Player = player
        self.hand_cards: List[Card] = cards
    def __hash__(self):
        return 0
    def __str__(self):
        cards_str = '|'.join(map(str, self.hand_cards))
        return f'CommunityHandDto(player={self.player}, hand={cards_str})'
