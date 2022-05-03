import tkinter as tk

from gui.chessboard import ChessBoard
from gui import GetImgPath
from config import *
from src.player import Player


class Brain:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board

        self.__grid: list[list[str]] = [['..' for _ in range(8)] for _ in range(8)]
        
        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)

        self.last_clicked: list[int] = [] # [x, y]
        self.last_selected: list[tuple[int, int]] = [] # [(r0, c0), (r1, c1), ...]
    
    @property
    def grid(self):
        return self.__grid
    
    @grid.setter
    def grid(self, newgrid: str):
        x = iter(newgrid)
        for i in range(8):
            for j in range(8):

                pl = next(x)
                pc = next(x)
                cell = self.board.cell(i, j)

                if pl==NULL or pc==NULL:
                    cell.clearimg()
                elif pl==self.player0.name:
                    self.player0.NewPiece(pc, i,j)
                    cell.newimg(tk.PhotoImage(file=GetImgPath(pl, pc)))
                elif pl==self.player1.name:
                    self.player1.NewPiece(pc, i,j)
                    cell.newimg(tk.PhotoImage(file=GetImgPath(pl, pc)))
                else:
                    raise Exception("Invalid player name")
                    
                cell.showimg()
                self.__grid[i][j] = f"{pl}{pc}"
    
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
            return '1' if self.player0.turn else '0'
        else:
            return '0' if self.player0.turn else '1'

    def Mouse_SLC(self, e: tk.Event):
        self.DeselectAll()
        if (loc:=self.board.xy2rc(e.x, e.y)): r, c = loc
        else: return

        if e.widget==self.board.board and self.__grid[r][c][0]==self.TurnOf():
            self.last_clicked.append((e.x, e.y))
            r, c = self.board.xy2rc(e.x, e.y)
            self.Select(r, c, CELL_SEL0)
    
    def Mouse_SRC(self, e: tk.Event):
        self.DeselectAll()
    
    def MouseDrag(self, e: tk.Event):
        pass

    def Select(self, r: int, c: int, fill: str):
        self.board.mark(r, c, fill)
        self.last_selected.append((r, c))
    
    def Deselect(self, r: int, c: int):
        self.board.cell(r, c).deselect()
    
    def DeselectAll(self):
        for loc in self.last_selected:
            self.Deselect(*loc)
        self.last_selected.clear()
    
    def SwitchTurn(self):
        if self.TurnOf()==self.player0.name:
            self.player0.turn = False
            self.player1.turn = True
        else:
            self.player0.turn = True
            self.player1.turn = False

    def Move(self, r0: int, c0: int, r1: int, c1: int):
        pass
    