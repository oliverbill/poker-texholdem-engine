from model.player import Player


class TournamentRank:
    def __init__(self, position: int, player: Player):
        self.position = position
        self.player = player

    def __str__(self):
        return f'TournamentRank(position={self.position},player={self.player})'
