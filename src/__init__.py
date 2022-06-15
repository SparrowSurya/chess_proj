import tkinter as tk
import copy

from gui.chessboard import ChessBoard
from gui.img import Image
from config import *
from config.const import *
from src.chessgrid import ChessGrid
from src.player import Player

class Brain:
    __slots__ = (
        'board', 'grid', 'Img',
        'player0', 'player1',
        'last_clicked', 'last_selected',
        'selected', 'pdrag', 'check', '__moves',
        'inMatch'
    )

    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board
        self.Img: Image = Image()
        self.inMatch: bool = False
        self.grid: ChessGrid = ChessGrid()

        
        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)

        self.last_clicked: list[int] = [-1, -1] # [x, y]
        self.last_selected: list[tuple[int, int]] = [] # [(r0, c0), (r1, c1), ...]

        self.selected: int = 0 # 0-nothing; 1-active: -1:passive
        self.pdrag: bool  = None

        self.check: Player = None

        self.__moves: dict[tuple, tuple] = {} # to pre fetch moves (also used for cache and end game detection)

    
    def NewGrid(self, newgrid: str):
        """sets the image as per the newgrid"""
        self.grid.grid = newgrid
        g = iter(self.grid)

        for i in range(8):
            for j in range(8):

                pl, pc = next(g)
                cell = self.board.cell(i, j)
                cell.showimg()

                if (pid:=f"{pl}{pc}")==NULL:
                    cell.clearimg()
                elif pl==self.player0:
                    self.player0.NewPiece(pc, i,j)
                    cell.newimg(self.Img[pl, pc], pid)
                elif pl==self.player1:
                    self.player1.NewPiece(pc, i,j)
                    cell.newimg(self.Img[pl, pc], pid)
                else:
                    raise Exception(f"Invalid player name: pid={pid}")

    def StartDefault(self, p1: bool = True):
        """to start a 1v1 match"""
        # reset board pieces 
        self.NewGrid(DEFAULT_GRID)
        if p1:
            self.player0.turn = False
            self.player1.turn = True
        else:
            self.player0.turn = True
            self.player1.turn = False
        self.inMatch = True
        self.moves_pre_fetch()
    
    def TurnOf(self, rev: bool=False):
        """returns the player object having current turn"""
        if rev:
            return self.player1 if self.player0.turn else self.player0
        else:
            return self.player0 if self.player0.turn else self.player1

    def Mouse_SLC(self, e: tk.Event):
        """bind event with single left click"""
        if not self.inMatch: return
        
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
            elif self.grid[r, c][0]==self.TurnOf() and (r,c)!=self.last_selected[0]:
                loc = self.board.xy2rc(e.x, e.y)
                self.DeselectAll()
                Epos, Apos = self.__moves[loc]

                self.Select(*loc, CELL_SEL0)
                for i, j in Epos:
                    self.Select(i, j, CELL_SEL1)
                for i, j in Apos:
                    self.Select(i, j, KILL)
                self.selected = 1

        else:
            if e.widget==self.board.board and self.grid[r, c][0]==self.TurnOf(): # HIGHLIGHT MOVES 
                loc = self.board.xy2rc(e.x, e.y)
                Epos, Apos = self.__moves[loc]

                self.Select(*loc, CELL_SEL0)
                for i, j in Epos:
                    self.Select(i, j, CELL_SEL1)
                for i, j in Apos:
                    self.Select(i, j, KILL)
                self.selected = 1
        self.pdrag = None

    def MouseDrag(self, e: tk.Event):
        """bind event for left click drag"""
        if not self.inMatch: return
        
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
        if not self.inMatch: return
        
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
        if not self.inMatch: return
        
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

        if en==(pid1:=self.grid[r1, c1])[0]: # KILL
            en.GetPiece(r1, c1, pid1[1]).alive = False
        
        if self.check: # UNCHECK KING
            self.board.cell(*(self.check.pieces[KING][0].loc)).uncheck()

        pc = fr.GetPiece(r0, c0)
        pc.move(r1, c1)
        pid2 = self.grid[r1, c1] = self.grid[r0, c0]
        del self.grid[r0, c0]
        self.board.move(r0, c0, r1, c1, self.grid[r1, c1])

        if self.grid[r1, c1][1]==PAWN and pc.canmove is False: # PAWN PROMOTION 
            self.board.AskPromotion(self.Promote, player=fr, pos=(r1,c1))

    def Promote(self, *, player: Player, rank: str, pos: tuple[int]):
        r, c = pos
        pid = f"{player.name}{rank}"
        player.Promote(*pos, rank)
        self.board.cell(*pos).newimg(self.Img[player.name, rank], pid)
        self.grid[r, c] = pid 

    def SwitchTurn(self):
        """switches the turn of players and also checks the Check on king"""
        if self.TurnOf() == self.player0:
            self.player0.turn = False
            (pl:=self.player1).turn = True
        else:
            (pl:=self.player0).turn = True
            self.player1.turn = False

        print(self.grid)
        if self.IsCheck(pl):
            self.check = pl
            pc = pl.pieces[KING][0]
            self.board.cell(*(pc.loc)).select(CHECK)

    def IsCheck(self, player: Player, *, move: tuple = None, i: int = 0):
        """checks the Check on player's king
        move: [r0, c0, r1, c1] moves the piece(temporary)
        :i is used to get the king if player has more than one king"""
        r, c = player.pieces[KING][i].loc

        grid = self.grid.grid
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
            else:
                continue
            if pid[1] is KING:
                return True
        
        for dr, dc in MARCH[KNIGHT]: # knight
            if (i:=r+dr) not in range(8) and (j:=c+dc) not in range(8):
                if (pid:=grid[i][j])[0]!=player:
                    continue
            else:
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
        """filters the move: Epos-empty, Apos-attack, Ipos-initial"""
        Fpos = [[], []]
        for i, pos in enumerate((Epos, Apos)):
            for r, c in pos:
                if self.IsCheck(self.TurnOf(), move=(*Ipos, r, c)):
                    continue
                else:
                    Fpos[i].append((r, c))
        return Fpos
    
    def moves_pre_fetch(self) -> bool:
        """stores the moves and returns bool value if there is no move to move"""
        res = False
        pl = self.TurnOf()
        self.__moves.clear()

        for pcs in pl.pieces.values():
            for pc in pcs:
                if pc.alive:
                    loc = pc.loc
                    e,a = self.FilterMoves(*(pc.moves(self.grid)), loc)
                    self.__moves[loc] = (e,a)
                    res = e or a or res
        return not res
    
    def EndMatch(self):
        """determines whether game should be running or stopped"""
        if self.moves_pre_fetch(): # 0 moves
            print("[MATCH ENDED]:- no moves to play")
            return

        fr, en = self.TurnOf(), self.TurnOf(True)
        fd, ed = fr.alives, en.alives
        stat = { KING: [0, 0], QUEEN: [0, 0], BISHOP: [0, 0], KNIGHT: [0, 0], ROOK: [0, 0], PAWN: [0, 0]} # [fr, en]

        for row in self.grid.grid:
            for (pl, pc) in row:
                if pl == pc: continue # to prevent NULL
                if pl is fr:
                    stat[pc][0] += 1
                else:
                    stat[pc][1] += 1

        # special cases
        if fd == ed == 1:
            print("[MATCH ENDED]:- king vs king")
            return

        elif (fd==2 and stat[QUEEN][0]==0 and en==1) or (en==2 and stat[QUEEN][1]==0 and fd==1):
            print("[MATCH ENDED]:- king vs minor piece with king")
            return

        elif (stat[KNIGHT][0]==2 and fd==3 and en==1) or (stat[KNIGHT][1]==2 and en==3 and fd==1):
            print("[MATCH ENDED]:- king and 2 knights vs king")
            return
        
        elif (fd==2 and en==2 and stat[QUEEN][0]==0) or (en==2 and fd==2 and stat[QUEEN][1]==0):
            print("[MATCH ENDED]:- king and minor piece vs king and minor piece")
            return

        elif (fd==1 and ed>1) or (en==1 and fd>1):
            print("[MATCH ENDED]:- lone king vs all the pieces")
            return
