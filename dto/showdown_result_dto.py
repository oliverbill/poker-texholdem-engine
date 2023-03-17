from dataclasses import dataclass
from typing import List

from dto.showdowncards_dto import ShowdownCardsDto

@dataclass
class ShowdownResultDto:
    winner_hands: List[ShowdownCardsDto]
    loser_hands: List[ShowdownCardsDto]

