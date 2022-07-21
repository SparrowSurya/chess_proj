from src.piece import *
from const import KING, QUEEN, KNIGHT, BISHOP, ROOK, PAWN, P1
from src.piece import Piece


class Player:

    def __init__(self, name: str):
        self.name: str = name

        self.turn: bool = False
        self.last_move: list[int, int, int, int] = [] # [r0, c0, r1, c1]

        self.__alive = 0
        self.__dead = 0
        self.pieces: dict[str, list[Piece]] = {
            KING  : [],
            QUEEN : [],
            KNIGHT: [],
            BISHOP: [],
            ROOK  : [],
            PAWN  : []
        }
    
    def __str__(self):
        return self.name

    def __eq__(self, name: str):
        return self.name == name
    
    @property
    def alives(self):
        return self.__alive

    @property
    def deaths(self):
        return self.__dead

    def IsOwner(self, piece_id: str):
        return piece_id[0] == self.name
    
    def kill(self, r: int, c: int, piece: str = None):
        #! havent thought what to do if king is passed due to some reasons
        if (pc:=self.GetPiece(r, c, piece)).alive is True:
            pc.alive = False
            self.__dead += 1
            self.__alive -= 1

    def GetPiece(self, r: int, c: int, piece: str = None) -> Piece:
        pieces = self.pieces.keys() if piece is None else [piece]
        for key in pieces:
            for pic in self.pieces[key]:
                if pic.alive and pic.pos == (r, c):
                    return pic

    def MovePiece(self, r0: int, c0: int, r1: int, c1: int):
        self.GetPiece(r0, c0).goto(r1, c1)
        self.last_move = [r0, c0, r1, c1]

    def NewPiece(self, piece: str, r: int, c: int):
        if piece==KING and self.pieces.get(KING):
            raise Exception(
                "[KING OVERLOAD] \n",
                "Player already has a king"
            )
        self.__NewPiece(piece, r, c)
    
    def __NewPiece(self, piece: str, r: int, c: int):
        if piece is PAWN:
            self.pieces[piece].append(Piece(self, piece, r, c, step=-1 if self.name==P1 else 1))
        elif piece is KING:
            self.pieces[piece].append(Piece(self, piece, r, c, undercheck=False))
        else:
            self.pieces[piece].append(Piece(self, piece, r, c))
        self.__alive += 1

    def Promote(self, r: int, c: int, rank: str):
        pc = self.GetPiece(r, c, PAWN)
        self.pieces[PAWN].remove(pc)
        pc.promote(rank)
        self.pieces[rank].append(pc)

    def Reset(self, turn: bool = None):
        for pc in self.pieces.keys():
            self.pieces[pc].clear()
        self.turn = turn
        self.last_move = []
        self.__alive, self.__dead = 0, 0

