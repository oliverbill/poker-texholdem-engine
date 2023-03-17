from typing import List

from controller.table_hand_controller import TableHandController
from model.player import Player
from model.tournament import Tournament


tournament1 = Tournament()

player1 = Player(50000, 1, 'billyalves')
player2 = Player(50000, 2, 'abreuLisinho')
player3 = Player(50000, 3, 'fidel')
tournament1.register_player(player1)
tournament1.register_player(player2)
tournament1.register_player(player3)
tournament1.start()

hands_controllers: List[TableHandController] = list()
for table in tournament1.get_tables():
    hands_controllers.append(TableHandController(table, tournament1))


