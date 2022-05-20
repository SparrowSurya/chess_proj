from src.piece import *
from gui.chessboard import ChessBoard
from config.const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN
from src.piece import King, Queen, Knight, Bishop, Rook, Pawn

PIECE: dict[str, type] = {
    KING: King,
    QUEEN: Queen,
    KNIGHT: Knight,
    BISHOP: Bishop,
    ROOK: Rook,
    PAWN: Pawn
}

class Player:
    __slots__ = ('board', 'name', 'turn', 'last_move', '__stats', 'pieces')

    def __init__(self, board: ChessBoard, name: str):
        self.board: ChessBoard = board
        self.name: str = name

        self.turn: bool = False
        self.last_move: list[int] = [] # [r0, c0, r1, c1]

        self.__stats: list[int] = [0, 0] # [total, dead]
        self.pieces: dict[str, list[King|Queen|Knight|Rook|Bishop|Pawn]] = {
            KING  : [],
            QUEEN : [],
            KNIGHT: [],
            BISHOP: [],
            ROOK  : [],
            PAWN  : []
        }
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, name: str):
        return self.name == name
    
    @property
    def alives(self):
        return self.__stats[0] - self.__stats[1]
    
    @property
    def total(self):
        return self.__stats[0]

    @property
    def deaths(self):
        return self.__stats[1]

    def IsOwner(self, piece_id: str):
        return piece_id[0] == self.name
    
    def kill(self, r: int, c: int, pic: str = None):
        if (pc:=self.GetPiece(r, c, pic)).alive is True:
            pc.alive = False
            self.__stats[1] += 1

    def GetPiece(self, r: int, c: int, piece: str = None):
        if piece is None:
            for key in self.pieces.keys():
                for pic in self.pieces[key]:
                    if pic.alive and pic.r == r and pic.c == c:
                        return pic
        else:
            for pic in self.pieces[piece]:
                if pic.alive and pic.r == r and pic.c == c:
                    return pic

    def MovePiece(self, r0: int, c0: int, r1: int, c1: int):
        piece = self.GetPiece(r0, c0)
        piece.move(r1, c1)

    def NewPiece(self, piece: str, r: int, c: int):
        if piece==KING and self.pieces.get(KING):
            raise Exception("Player already has a king")
        obj = PIECE[piece]
        self.pieces[piece].append(obj(self.name, r, c))
        self.__stats[0] += 1

    def Promote(self, ):
        pass
