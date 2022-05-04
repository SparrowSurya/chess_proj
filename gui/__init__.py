from config.const import  KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN
from config import IPATH

def GetImgPath(player: str, piece: str):
    IMG = {
    '0': {
            KING: '0K.png',
            QUEEN: '0Q.png',
            KNIGHT: '0N.png',
            BISHOP: '0B.png',
            ROOK: '0R.png',
            PAWN: '0P.png'
        },
    '1': {
            KING: '1K.png',
            QUEEN: '1Q.png',
            KNIGHT: '1N.png',
            BISHOP: '1B.png',
            ROOK: '1R.png',
            PAWN: '1P.png'
        }
    }
    return f"{IPATH}\{IMG[player][piece]}"