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

        self.last_clicked: list[int] = [-1, -1] # [x, y]
        self.last_selected: list[tuple[int, int]] = [] # [(r0, c0), (r1, c1), ...]

        self.selected: bool = False
        self.pdrag: bool  = None

        self.check: Player = None
    
    @property
    def grid(self):
        return self.__grid
    
    def show(self):
        print()
        for i in range(8):
            for j in range(8):
                print(self.__grid[i][j], end=' ')
            print()
        print()
    
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
                    raise Exception(f"Invalid player name: pid={pid}")
                    
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
            if cell.selected:
                i, j = self.last_selected[0]
                self.MovePiece(i, j, r, c)
                self.SwitchTurn()
            self.DeselectAll()

        elif self.selected and (r, c) == self.last_selected[0]:
            self.DeselectAll()

        elif e.widget==self.board.board and self.__grid[r][c][0]==self.TurnOf():
            self.DeselectAll()
            r, c = self.board.xy2rc(e.x, e.y)
            Epos, Apos = self.GetMoves(r, c)

            self.Select(r, c, CELL_SEL0)
            for i, j in Epos:
                self.Select(i, j, CELL_SEL1)
            for i, j in Apos:
                self.Select(i, j, KILL)
    
    def MouseDrag(self, e: tk.Event):
        x, y = self.last_clicked

        if self.pdrag:
            loc = self.last_selected[0]
            self.board.cell(*loc).move(e.x-x, e.y-y)
        elif self.pdrag is None:
            loc = self.board.xy2rc(*self.last_clicked)

            if loc is not None and self.board.cell(*loc).selected:
                cell = self.board.cell(*loc)
                ix, iy = cell.imcoords()
                cell.move(x-ix, y-iy)
                self.pdrag = True
            else:
                self.pdrag = False

        self.last_clicked = [e.x, e.y]
    
    def Mouse_LCR(self, e: tk.Event):
        if self.pdrag:
            loc = self.board.xy2rc(e.x, e.y)
            r0, c0 = self.last_selected[0]

            if loc is None:
                self.DeselectAll()
                self.pdrag = None
                self.board.cell(r0, c0).resetmove()
                return
            else:
                r1, c1 = loc

            cell = self.board.cell(r1, c1)
            if cell.selected and (r0, c0)!=(r1, c1):
                self.MovePiece(r0, c0, r1, c1)
                self.SwitchTurn()
            else:
                self.board.cell(r0, c0).resetmove()
            self.DeselectAll()
        self.pdrag = None
    
    def Mouse_SRC(self, e: tk.Event):
        self.DeselectAll()

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

    def GetMoves(self, r: int, c: int, rev: bool = False):
        pc = self.TurnOf(rev).GetPiece(r, c)
        return pc.moves(self.grid)

    def MovePiece(self, r0: int, c0: int, r1: int, c1: int):
        fr, en = self.TurnOf(), self.TurnOf(True)

        if en==(pid1:=self.__grid[r1][c1])[0]:
            en.GetPiece(r1, c1, pid1[1]).alive = False

        fr.GetPiece(r0, c0).move(r1, c1)
        self.__grid[r1][c1] = self.__grid[r0][c0]
        self.__grid[r0][c0] = NULL
        self.board.move(r0, c0, r1, c1, self.__grid[r1][c1])

    def SwitchTurn(self):
        if self.TurnOf() == self.player0:
            self.player0.turn = False
            (pl:=self.player1).turn = True
        else:
            (pl:=self.player0).turn = True
            self.player1.turn = False

        if self.IsCheck(pl):
            self.check = pl
            self.board.cell(*(pl.pieces[KING][0].loc)).select(CHECK)

    def IsCheck(self, player: Player, i: int=0):
        king = player.pieces[KING][i]
        r, c = king.loc

        for dr, dc in MARCH[BISHOP]: # bishop
            i, j = r+dr, c+dc
            while (i in range(8) and j in range(8)) and (pid:=self.__grid[i][j])[0]!=player:
                if pid[1] in (QUEEN, BISHOP):
                    return True
                i, j = i+dr, j+dc

        for dr, dc in MARCH[ROOK]: # rook
            i, j = r+dr, c+dc
            while (i in range(8) and j in range(8)) and (pid:=self.__grid[i][j])[0]!=player:
                if pid[1] in (QUEEN, ROOK):
                    return True
                i, j = i+dr, j+dc
        
        for dr, dc in MARCH[KING]: # king
            if (i:=r+dr) not in range(8) and (j:=c+dc) not in range(8) and (pid:=self.__grid[i][j])[0]!=player:
                continue
            if pid[1] is KING:
                return True
        
        for dr, dc in MARCH[KNIGHT]: # knight
            if (i:=r+dr) not in range(8) and (j:=c+dc) not in range(8) and (pid:=self.__grid[i][j])[0]!=player:
                continue
            if pid[1] is KNIGHT:
                return True
        
        d = -1 if player==P1 else 1
        if r+d in range(8) and c+1 in range(8): # pawn right
            pid=self.__grid[r+d][c+1]
            if pid[0] not in (NULL[0], player) and pid[1] == PAWN:
                return True
        if r+d in range(8) and c-1 in range(8): # pawn left
            pid=self.__grid[r+d][c-1]
            if pid[0] not in (NULL[0], player) and pid[1] == PAWN:
                return True

        return False

    def FilterMoves(self, ):
        pass