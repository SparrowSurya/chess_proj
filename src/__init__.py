import tkinter as tk

from gui.chessboard import ChessBoard
from gui import GetImgPath
from config import *
from config.const import *
from src.player import Player


class Brain:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board

        self.__grid: list[list[str]] = [[NULL for _ in range(8)] for _ in range(8)]
        
        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)

        self.last_clicked: list[int] = [] # [x, y]
        self.last_selected: list[tuple[int, int]] = [] # [(r0, c0), (r1, c1), ...]

        self.selected: bool = False
        self.mdrag: bool = False
    
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

                if (pid:=f"{pl}{pc}")==NULL:
                    cell.clearimg()
                elif pl==self.player0:
                    self.player0.NewPiece(pc, i,j)
                    cell.newimg(tk.PhotoImage(file=GetImgPath(pl, pc)), pid)
                elif pl==self.player1:
                    self.player1.NewPiece(pc, i,j)
                    cell.newimg(tk.PhotoImage(file=GetImgPath(pl, pc)), pid)
                else:
                    raise Exception("Invalid player name")
                    
                cell.showimg()
                self.__grid[i][j] = pid
    
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
            return self.player1 if self.player0.turn else self.player0
        else:
            return self.player0 if self.player0.turn else self.player1

    def Mouse_SLC(self, e: tk.Event):
        self.last_clicked = [e.x, e.y]
        loc = self.board.xy2rc(e.x, e.y)

        if loc is None:
            self.DeselectAll()
            return
        else:
            r, c = loc
            
        if self.selected and (cell:=self.board.cell(r, c)).pid[0] != self.TurnOf():
            cell = self.board.cell(r, c)
            if cell.selected:
                i, j = self.last_selected[0]
                self.Move(i, j, r, c)
                self.switch()
            self.DeselectAll()
        else:
            if e.widget==self.board.board and self.__grid[r][c][0]==self.TurnOf():
                self.DeselectAll()
                r, c = self.board.xy2rc(e.x, e.y)
                Epos, Apos = self.GetMoves(r, c)

                self.Select(r, c, CELL_SEL0)
                for i, j in Epos:
                    self.Select(i, j, CELL_SEL1)
                for i, j in Apos:
                    self.Select(i, j, KILL)
    
    def Mouse_SRC(self, e: tk.Event):
        self.DeselectAll()
    
    def MouseDrag(self, e: tk.Event):
        pass

    def Select(self, r: int, c: int, fill: str):
        self.board.mark(r, c, fill)
        self.last_selected.append((r, c))
        self.selected = True
    
    def Deselect(self, r: int, c: int):
        self.board.cell(r, c).deselect()
    
    def DeselectAll(self):
        for loc in self.last_selected:
            self.Deselect(*loc)
        self.last_selected.clear()
        self.selected = False
    
    def SwitchTurn(self):
        if self.TurnOf()==self.player0:
            self.player0.turn = False
            self.player1.turn = True
        else:
            self.player0.turn = True
            self.player1.turn = False

    def GetMoves(self, r: int, c: int, rev: bool = False):
        pc = self.TurnOf(rev).GetPiece(r, c)
        return pc.moves(self.grid)

    def Move(self, r0: int, c0: int, r1: int, c1: int):
        self.TurnOf().GetPiece(r0, c0).move(r1, c1)
        self.__grid[r1][c1] = self.grid[r0][c0]
        self.__grid[r0][c0] = NULL
        self.board.move(r0, c0, r1, c1, self.__grid[r1][c1])

    def switch(self):
        if self.TurnOf() == self.player0:
            self.player0.turn = False
            self.player1.turn = True
        else:
            self.player0.turn = True
            self.player1.turn = False
