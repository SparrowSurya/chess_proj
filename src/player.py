from src.piece import *
from gui.chessboard import ChessBoard

class Player:
    def __init__(self, board: ChessBoard, name: str):
        self.board: ChessBoard = board
        self.name: str = name

        self.turn: bool = False
        self.last_move: list[int] = [] # [r0, c0, r1, c1]
    

    # def isowner(self, piece):
    #     """returns true false and None if piece is empty"""
    #     return piece[0]==self.player[0] if piece else None
    
    # def _kill(self, r, c):
    #     """kills the piece at r,c"""
    #     piece_id = self.getpieceatRC(r,c)
    #     if piece_id is not None:
    #         # winsound.Beep(440, 280)
    #         piece_id.alive = False
    #         piece_id.r, piece_id.c = None,None
    
    # def getpieceatRC(self, r,c):
    #     """returns the piece id"""
    #     for i in range(8):
    #         if self.mains[i].pos()==(r,c):
    #             if self.mains[i].alive: return self.mains[i] 
    #         if self.pawns[i].pos()==(r,c):
    #             if self.pawns[i].alive: return self.pawns[i] 
    
    # def update_piece_position(self, ir, ic, fr, fc):
    #     """updates the piece location"""
    #     self.getpieceatRC(ir,ic).goto(fr, fc)

    # def init(self, pawns_row, pawns_dir, mains_row):
    #     """places the pieces at initial position"""
    #     self.__create_mains(mains_row)
    #     self.__create_pawns(pawns_row, pawns_dir)

    # def __create_pawns(self, r, _dir):
    #     self.pawns = []
    #     for c in range(8):
    #         self.pawns.append(self.__pawn(r,c,_dir))
    
    # def __pawn(self, r,c, _dir):
    #     """makes and returns pawn and automatically places that on board"""
    #     pawn = Pawn(self, [r, c], self.img_path[self.player[0]+'P'], _dir)
    #     self.board.writeimg(r, c, pawn.name, pawn.getimg())
    #     return pawn

    # def __create_mains(self, r):
    #     self.mains = []

    #     # rook 1
    #     self.rook_1 = Rook(self, [r, 0], self.img_path[self.player[0]+'R'])
    #     self.board.writeimg(r, 0, self.rook_1.name, self.rook_1.getimg())
    #     self.mains.append(self.rook_1)

    #     # knight 1
    #     self.knight_1 = Knight(self, [r, 1], self.img_path[self.player[0]+'N'])
    #     self.board.writeimg(r, 1, self.knight_1.name, self.knight_1.getimg())
    #     self.mains.append(self.knight_1)

    #     # bishop 1
    #     self.bishop_1 = Bishop(self, [r, 2], self.img_path[self.player[0]+'B'])
    #     self.board.writeimg(r, 2, self.bishop_1.name, self.bishop_1.getimg())
    #     self.mains.append(self.bishop_1)

    #     # queen
    #     self.queen = Queen(self, [r, 3], self.img_path[self.player[0]+'Q'])
    #     self.board.writeimg(r, 3, self.queen.name, self.queen.getimg())
    #     self.mains.append(self.queen)

    #     # king
    #     self.king = King(self, [r, 4], self.img_path[self.player[0]+'K'])
    #     self.board.writeimg(r, 4, self.king.name, self.king.getimg())
    #     self.mains.append(self.king)

    #     # bishop 2
    #     self.bishop_2 = Bishop(self, [r, 5], self.img_path[self.player[0]+'B'])
    #     self.board.writeimg(r, 5, self.bishop_2.name, self.bishop_2.getimg())
    #     self.mains.append(self.bishop_2)

    #     # knight 1
    #     self.knight_2 = Knight(self, [r, 6], self.img_path[self.player[0]+'N'])
    #     self.board.writeimg(r, 6, self.knight_2.name, self.knight_2.getimg())
    #     self.mains.append(self.knight_2)

    #     # rook 2
    #     self.rook_2 = Rook(self, [r, 7], self.img_path[self.player[0]+'R'])
    #     self.board.writeimg(r, 7, self.rook_2.name, self.rook_2.getimg())
    #     self.mains.append(self.rook_2)

    # def pawn_promotion(self, pawn:Pawn, to:str):
    #     if to.lower()=='queen': pawn.__class__ = Queen
    #     elif to.lower()=='knight': pawn.__class__ = Knight
    #     elif to.lower()=='bishop': pawn.__class__ = Bishop
    #     elif to.lower()=='rook': pawn.__class__ = Rook
    #     else: raise Exception(f"unknown option -to as {to}")
    #     pawn.img_path = self.img_path[self.player[0]+pawn.alias]
    #     self.board.writeimg(*pawn.pos(),pawn.name, pawn.getimg())
