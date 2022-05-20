import tkinter as tk
import copy

from gui.chessboard import ChessBoard
from gui import GetImgPath
from config import *
from config.const import *
from src.player import Player


class Brain:
    __slots__ = (
        'board', '__grid',
        'player0', 'player1',
        'last_clicked', 'last_selected',
        'selected', 'pdrag', 'check', '_moves'
    )

    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board

        self.__grid: list[list[str]] = [[NULL for _ in range(8)] for _ in range(8)]
        
        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)

        self.last_clicked: list[int] = [-1, -1] # [x, y]
        self.last_selected: list[tuple[int, int]] = [] # [(r0, c0), (r1, c1), ...]

        self.selected: int = 0 # 0-nothing; 1-active: -1:passive
        self.pdrag: bool  = None

        self.check: Player = None

        self._moves: dict = {} # to pre fetch moves (also used for cache and end game detection)
    
    @property
    def grid(self):
        return self.__grid
    
    def show(self):
        """prints chess grid on console"""
        print()
        for i in range(8):
            for j in range(8):
                print(self.__grid[i][j], end=' ')
            print()
        print()
    
    @grid.setter
    def grid(self, newgrid: str):
        """sets the image as per the newgrid definition"""
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
        """to start a 1v1 match"""
        # reset board pieces 
        self.grid = DEFAULT_GRID
        if p1:
            self.player0.turn = False
            self.player1.turn = True
        else:
            self.player0.turn = True
            self.player1.turn = False
        
        self.moves_pre_fetch()
    
    def TurnOf(self, rev: bool=False):
        """returns the player object having current turn"""
        if rev:
            return self.player1 if self.player0.turn else self.player0
        else:
            return self.player0 if self.player0.turn else self.player1

    def Mouse_SLC(self, e: tk.Event):
        """bind event with single left click"""
        self.last_clicked = [e.x, e.y]
        loc = self.board.xy2rc(e.x, e.y)

        if loc is None:
            self.DeselectAll()
            return
        else:
            r, c = loc
        
        if self.selected:
            self.selected = -1
            if self.board.cell(r,c).selected and (r,c)!=self.last_selected[0]:
                self.MovePiece(*self.last_selected[0], r, c)
                self.DeselectAll()
                self.SwitchTurn()
                self.EndMatch()
            elif self.grid[r][c][0]==self.TurnOf() and (r,c)!=self.last_selected[0]:
                loc = self.board.xy2rc(e.x, e.y)
                self.DeselectAll()
                Epos, Apos = self._moves[loc]

                self.Select(*loc, CELL_SEL0)
                for i, j in Epos:
                    self.Select(i, j, CELL_SEL1)
                for i, j in Apos:
                    self.Select(i, j, KILL)
                self.selected = 1

        else:
            if e.widget==self.board.board and self.__grid[r][c][0]==self.TurnOf(): # HIGHLIGHT MOVES 
                loc = self.board.xy2rc(e.x, e.y)
                Epos, Apos = self._moves[loc]

                self.Select(*loc, CELL_SEL0)
                for i, j in Epos:
                    self.Select(i, j, CELL_SEL1)
                for i, j in Apos:
                    self.Select(i, j, KILL)
                self.selected = 1
        self.pdrag = None

    def MouseDrag(self, e: tk.Event):
        """bind event for left click drag"""
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
        """bind event for mouse left click release"""
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
                self.DeselectAll()
                self.SwitchTurn()
                self.EndMatch()
            else:
                self.board.cell(r0, c0).resetmove()
                self.DeselectAll()

        elif self.pdrag is None and self.selected == -1:
            self.DeselectAll()

    
    def Mouse_SRC(self, e: tk.Event):
        """bind event with single right click"""
        self.DeselectAll()

    def Select(self, r: int, c: int, fill: str):
        """to select the cell"""
        self.board.mark(r, c, fill)
        self.last_selected.append((r, c))
    
    def Deselect(self, r: int, c: int):
        """to deselect the cell"""
        self.board.cell(r, c).deselect()
    
    def DeselectAll(self):
        """to deselect all the selected cells"""
        for loc in self.last_selected:
            self.Deselect(*loc)
        self.last_selected.clear()
        self.selected = 0

    def MovePiece(self, r0: int, c0: int, r1: int, c1: int):
        """moves the piece"""
        fr, en = self.TurnOf(), self.TurnOf(True)

        if en==(pid1:=self.__grid[r1][c1])[0]: # KILL
            en.GetPiece(r1, c1, pid1[1]).alive = False
        
        if self.check: # UNCHECK KING
            self.board.cell(*(self.check.pieces[KING][0].loc)).uncheck()

        fr.GetPiece(r0, c0).move(r1, c1)
        self.__grid[r1][c1] = self.__grid[r0][c0]
        self.__grid[r0][c0] = NULL
        self.board.move(r0, c0, r1, c1, self.__grid[r1][c1])

    def SwitchTurn(self):
        """switches the turn of players"""
        if self.TurnOf() == self.player0:
            self.player0.turn = False
            (pl:=self.player1).turn = True
        else:
            (pl:=self.player0).turn = True
            self.player1.turn = False

        self.show()
        if self.IsCheck(pl):
            self.check = pl
            pc = pl.pieces[KING][0]
            self.board.cell(*(pc.loc)).select(CHECK)

    def IsCheck(self, player: Player, *, move: tuple = None, i: int = 0):
        """
        checks the Check on player's king \n
        move: [r0, c0, r1, c1] moves the piece(temporary) \n
        i is used to get the king if player has more than one king \n
        """

        king = player.pieces[KING][i]
        r, c = king.loc

        grid = copy.deepcopy(self.grid)
        if move is not None:
            r0, c0, r1, c1 = move
            grid[r1][c1] = grid[r0][c0]
            grid[r0][c0] = NULL
            if grid[r1][c1]==f"{player}{KING}":
                r, c = r1, c1

        for dr, dc in MARCH[BISHOP]: # bishop
            i, j = r+dr, c+dc
            while (i in range(8) and j in range(8)) and (pid:=grid[i][j])[0]!=player:
                if pid[1] in (QUEEN, BISHOP):
                    return True
                i, j = i+dr, j+dc

        for dr, dc in MARCH[ROOK]: # rook
            i, j = r+dr, c+dc
            while (i in range(8) and j in range(8)) and (pid:=grid[i][j])[0]!=player:
                if pid[1] in (QUEEN, ROOK):
                    return True
                i, j = i+dr, j+dc
        
        for dr, dc in MARCH[KING]: # king
            if (i:=r+dr) not in range(8) and (j:=c+dc) not in range(8):
                if (pid:=grid[i][j])[0]!=player:
                    continue
            if pid[1] is KING:
                return True
        
        for dr, dc in MARCH[KNIGHT]: # knight
            if (i:=r+dr) not in range(8) and (j:=c+dc) not in range(8):
                if (pid:=grid[i][j])[0]!=player:
                    continue
            if pid[1] is KNIGHT:
                return True
        
        d = -1 if player==P1 else 1
        if r+d in range(8) and c+1 in range(8): # pawn right
            pid=grid[r+d][c+1]
            if pid[0] not in (NULL[0], player) and pid[1] == PAWN:
                return True
        if r+d in range(8) and c-1 in range(8): # pawn left
            pid=grid[r+d][c-1]
            if pid[0] not in (NULL[0], player) and pid[1] == PAWN:
                return True

        return False

    def FilterMoves(self, Epos, Apos, Ipos):
        """to filter move"""
        Fpos = [[], []]
        for i, pos in enumerate((Epos, Apos)):
            for r, c in pos:
                if self.IsCheck(self.TurnOf(), move=(*Ipos, r, c)):
                    continue
                else:
                    Fpos[i].append((r, c))
        return Fpos
    
    def moves_pre_fetch(self) -> bool:
        """returns bool value if there is no move to move"""
        res = False
        pl = self.TurnOf()

        for pcs in pl.pieces.values():
            for pc in pcs:
                if pc.alive:
                    loc = pc.loc
                    e,a = self.FilterMoves(*(pc.moves(self.grid)), loc)
                    self._moves[loc] = (e,a)
                    res = e or a or res
        return not res
    
    def EndMatch(self):
        """determines whether game should be running or stopped"""
        self._moves.clear()

        if self.moves_pre_fetch(): # 0 moves
            print("MATCH ENDED")

        fr, en = self.TurnOf().deaths, self.TurnOf().deaths
        left = {
            KING: [],
            QUEEN: [],
            BISHOP: [],
            KNIGHT: [],
            ROOK: [],
            PAWN: []
        }
        # king vs king >>> 1,1
        # king+minor piece with king >>> 1, 2
        # lone king vs all the pieces >>> 1, 1+
        # king+2knights vs king >>> 1, 3
        # king+minor piece vs king+minor piece >>> 2, 2