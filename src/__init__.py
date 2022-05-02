import tkinter as tk

from gui.chessboard import ChessBoard
from config import *
from src.player import Player


class ctx:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board

        self.last_selected_cell = [] 
        self.last_clicked_loc = []
    
    def Select(self, r: int, c: int, fill: str):
        """selects the given location"""
        self.board.mark(r, c, fill)
        self.last_selected_cell.append((r, c))
    
    def Deselect(self, r: int, c: int):
        """deselects the given location"""
        self.board.cell(r, c).deselect()
    
    def deselect_all(self):
        """deselects all the selected cells"""
        for loc in self.last_selected_cell:
            self.Deselect(*loc)
        self.last_selected_cell.clear()

    def MLRC(self, e: tk.Event):
        self.deselect_all()

        if e.widget==self.board.board:
            self.last_clicked_loc.append((e.x, e.y))
            r, c = self.board.xy2rc(e.x, e.y)
            return self.Select(r, c, CELL_SEL0)
    
    def MSRC(self, e: tk.Event):
        self.deselect_all()


class Brain:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board
        self.ctx: ctx = ctx(self.board)

        self.__grid: list[list[str]] = [['..' for _ in range(8)] for _ in range(8)]
        
        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)
    
    @property
    def grid(self):
        return self.__grid
    
    @grid.setter
    def grid(self, newgrid: str):
        x = iter(newgrid)
        for i in range(8):
            for j in range(8):
                self.__grid[i][j] = f"{next(x)}{next(x)}"
        # update the grid
    
    def StartDefault(self, p1: bool = True):
        # reset board pieces 
        self.grid = DEFAULT_GRID
        if p1:
            self.player0.turn = False
            self.player1.turn = True
        else:
            self.player0.turn = True
            self.player1.turn = False
    
    def TurnOf(self, rev: bool=False):
        if rev:
            return '0' if self.player0.turn else '1'
        else:
            return '1' if self.player0.turn else '0'
    
    def GetPieceID(self, x: int, y: int):
        loc = self.board.xy2rc(x, y)
        if loc is not None:
            r, c = loc
            return self.__grid[r][c]
        return NULL

    def Mouse_SLC(self, e: tk.Event):
        if self.GetPieceID(e.x, e.y)[0]==self.TurnOf():
            self.ctx.MLRC(e)
    
    def Mouse_SRC(self, e: tk.Event):
        if self.GetPieceID(e.x, e.y)[0]==self.TurnOf():
            self.ctx.MSRC(e)
    
    def MouseDrag(self, e: tk.Event):
        pass

    