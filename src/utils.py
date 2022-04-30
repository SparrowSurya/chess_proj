from config import REFRENCE as ref

class Id(str):
    def __init__(self, name: str) -> None:
        if isinstance(name, str):
            self.__id: str = name
        else:
            raise Exception("accepts only string values")
    
    def __call__(self) -> str:
        return self.__id

    def __eq__(self, __x: object) -> bool:
        return super().__eq__(__x)


class _Ref:
    @property
    def p0(self): return ref['player0']
    @property
    def p1(self): return ref['player1']
    @property
    def king(self): return ref['king']
    @property
    def queen(self): return ref['queen']
    @property
    def knight(self): return ref['knight']
    @property
    def bishop(self): return ref['bishop']
    @property
    def rook(self): return ref['rook']
    @property
    def pawn(self): return ref['pawn']


class utl(_Ref):

    def getplayer(self, Id: Id):
        pl = {
            '0': self.p0,
            '1': self.p1,
            '.': None
        }
        return pl[Id[0]]

    def getpiece(self, Id: Id):
        pc = {
            'K': self.king,
            'Q': self.queen,
            'B': self.bishop,
            'R': self.rook,
            'N': self.knight,
            'P': self.pawn,
            '.': None
        }
        return pc[Id[1]]

x = Id('a')
print(x=='a')