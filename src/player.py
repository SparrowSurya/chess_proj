from src.piece import *
from gui.chessboard import ChessBoard

class Player:
    def __init__(self, board: ChessBoard, name: str):
        self.board: ChessBoard = board
        self.name: str = name

        self.turn: bool = False
        self.last_move: list[int] = [] # [r0, c0, r1, c1]
    
    def IsOwner(self, piece_id: str):
        return piece_id[0] == self.name
    
    def kill(self, r: int, c: int):
        pass

    def GetPiece(self, r: int, c: int):
        pass

    def MovePiece(self, r0: int, c0: int, r1: int, c1: int):
        pass

    def NewPiece(self, ):
        pass

    def Promote(self, ):
        pass
