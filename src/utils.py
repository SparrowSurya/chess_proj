PLAYER0 = '0'
PLAYER1 = '1'

KING = 'K'
QUEEN = 'Q'
KNIGHT = 'N'
BISHOP = 'B'
ROOK = 'R'
PAWN = 'P'


def getplayer(_id: str):
    pl = {
        '0': PLAYER0,
        '1': PLAYER1,
        '.': None
    }
    return pl[_id[0]]

def getpiece(_id: str):
    pc = {
        'K': KING,
        'Q': QUEEN,
        'B': BISHOP,
        'R': ROOK,
        'N': KNIGHT,
        'P': PAWN,
        '.': None
    }
    return pc[_id[1]]
