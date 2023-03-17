class Blind:
    def __init__(self, small_blind: int, minutes):
        self.__time = minutes
        self.__small = small_blind
        self.__big = small_blind * 2
        self.__ante = small_blind * 2
    
    def small_blind(self) -> int:
        return self.__small
    
    def big_blind(self) -> int:
        return self.__big
    
    def ante(self) -> int:
        return self.__ante
    @staticmethod
    def generate_blinds():
        out = {1: Blind(5, 15),
               2: Blind(10, 15),
               3: Blind(15, 15),
               4: Blind(20, 15),
               5: Blind(25, 15),
               6: Blind(50, 15),
               7: Blind(75, 15),
               8: Blind(100, 15),
               9: Blind(150, 10),
               10: Blind(200, 10),
               11: Blind(300, 10),
               12: Blind(400, 10),
               13: Blind(500, 10),
               14: Blind(600, 10),
               15: Blind(800, 10),
               16: Blind(1000, 10),
               17: Blind(1200, 10),
               18: Blind(1500, 10),
               19: Blind(2000, 10),
               20: Blind(2500, 10),
               21: Blind(3000, 10),
               22: Blind(3500, 10),
               23: Blind(4000, 10),
               24: Blind(4500, 10),
               25: Blind(5000, 10),
               26: Blind(10000, 10),
               27: Blind(15000, 10),
               28: Blind(20000, 10),
               29: Blind(25000, 10),
               30: Blind(30000, 10),
               31: Blind(40000, 10),
               32: Blind(50000, 10),
               33: Blind(60000, 10),
               34: Blind(70000, 10),
               35: Blind(80000, 10),
               36: Blind(90000, 10),
               37: Blind(100000, 10)}
        return out

    def __str__(self):
        return f'Blind(time={self.__time},small_blind={self.__small},big_blind={self.__big},ante={self.__ante})'
