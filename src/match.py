from collections import namedtuple

from gui.img import Image
from gui.chessboard import ChessBoard
from src.chessgrid import ChessGrid
from src.player import Player
from config.const import *
from lib.utils import *

class Match:

    def __init__(self, chessboard: ChessBoard, chessgrid: ChessGrid, image_dict: Image):
        self.board = chessboard
        self.grid = chessgrid
        self.img = image_dict
        
        self.p0: Player = Player(P0)
        self.p1: Player = Player(P1)

        self.__status: str = IDLE

        self.last_loc: list[int, int] = [-1, -1] # x, y
        self.last_sel: list[tuple[int, int]] = [] # [(rn, cn), ...]

        self.drag: bool = None
        self.check: Player = None

        self.__moves: dict[tuple, tuple] = {} # (r, c) -> (moves, attacks)


    @property
    def stats(self):
        """Returns current stats if players are playing."""
        if self.status==IDLE: return
        fr, en = self.TurnOf(), self.TurnOf(True)
        info = namedtuple('info', ['status', 'turn', 'check', 'captures'])
        return info(self.__status, fr.name, self.check.name==fr, (fr.deaths,en.deaths))
    
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new: str):
        """FOr handelling interruption between the match."""
        # taking decision based on the status

    def Start(self, setup: str = None):
        """Start game with given arrangement."""
        self.grid.grid = setup if setup is not None else DEFAULT_GRID
        self.p0.Reset(False) and self.p1.Reset(True)
        itr = iter(self.grid)

        for r in range(8):
            for c in range(8):
                if (pid:=next(itr))!=NULL:
                    self.LoadPiece(r, c, *pid)

        self.__status = PLAY
        self.IsMatchEnd()
        self.PreFetchMoves()
        self.Check()
    
    def LoadPiece(self, r: int, c: int, player: str, piece: str):
        """Loads the piece in player pieces."""
        pid = get_pid(player, piece)
        self.board.cell(r, c).newimg(self.img[pid], pid)
        if player==P0: self.p0.NewPiece(piece, r, c)
        elif player==P1: self.p1.NewPiece(piece, r, c)
        else:
            raise Exception(
                "[Invalid Player name] \n",
                f"player name: {player}"
            )
    
    def TurnOf(self, rev: bool=False):
        """returns the player object having current turn"""
        if rev:
            return self.p1 if self.p0.turn else self.p0
        else:
            return self.p0 if self.p0.turn else self.p1
    
    def SwitchTurn(self) -> Player:
        """switches the turn of players and also checks the Check on king"""
        if self.TurnOf() == self.p0:
            self.p0.turn = False
            self.p1.turn = True
        else:
            self.p0.turn = True
            self.p1.turn = False
        print(self.grid)

    def Check(self):
        """Checks the check on king and displays if there."""
        pl = self.TurnOf()
        if self.IsCheck(pl):
            print("[CHECK]")
            self.check = pl
            pc = pl.pieces[KING][0]
            self.board.cell(*(pc.loc)).c
    
    def Clicked(self, click_type: str, x: int, y: int):
        """Takes Click decision."""
        func = {
            '<SLC>': self._SLC,
            '<LD>' : self._LD,
            '<LCR>': self._LCR,
            '<SRC>': self._SRC
        }[click_type]
        func(x, y)
    
    def _SLC(self, x: int, y: int):
        """Underlying function for mouse single left click."""
        self.last_loc = [x, y]
        r, c = self.board.xy2rc(x, y)
        if self.last_sel:
            self.sel_flag = -1
            if (r,c) in self.last_sel[1:]:
                self.Move(*self.last_sel[0], r, c)
                self.Deselect(all=True)
                self.SwitchTurn()
                self.IsMatchEnd()
            elif (r, c) == self.last_sel[0]:
                self.MakeSelections(r, c)
                self.sel_flag = 1
            elif self.grid[r, c]!=NULL:
                self.MakeSelections(r, c)
                self.sel_flag = 1
            else:
                self.Deselect(all=True)
                self.drag = False
                return
        else:
            if self.grid[r, c][0] == self.TurnOf():
                self.MakeSelections(r, c)
                self.sel_flag = 1
        self.drag = None
    
    def _LD(self, x: int, y: int):
        """Underlying function for mouse left click drag."""
        x1, y1 = self.last_loc
        if self.drag:
            pos = self.last_sel[0]
            self.board.cell(*pos).move(x-x1, y-y1)
        elif self.drag is None:
            pos = self.board.xy2rc(*self.last_loc)
            if pos in self.last_sel:
                cell = self.board.cell(*pos)
                ix, iy = cell.COORDS_IMG
                cell.move(x-ix, y-iy)
                self.drag = True
            else:
                self.drag = False
        self.last_loc = [x, y]

    def _LCR(self, x: int, y: int):
        """Underlying function for mouse left click release."""
        if self.drag:
            pos = self.board.xy2rc(x, y)
            r0, c0 = self.last_sel[0]

            if pos is None:
                self.Deselect(all=True)
                self.drag = None
                self.board.cell(r0, c0).reset_move()
                return
            else:
                r1, c1 = pos

            cell = self.board.cell(r1, c1)
            if cell.selected and (r0, c0)!=(r1, c1):
                self.Move(r0, c0, r1, c1)
                self.Deselect(all=True)
                self.SwitchTurn()
                self.IsMatchEnd()
            else:
                self.board.cell(r0, c0).reset_move()
                self.Deselect(all=True)

        elif self.drag is None and self.sel_flag == -1:
            self.Deselect(all=True)

    def _SRC(self, x: int, y: int):
        """Underlying function for mouse right click."""
        self.Deselect(all=True)
        
    def MakeSelections(self, r: int, c: int):
        if self.grid[r, c] == NULL: return False
        self.Deselect(all=True)
        Epos, Apos = self.__moves[(r, c)]
        self.Select(r, c, SELECT)
        for i, j in Epos:
            self.Select(i, j, HIGHLIGHT)
        for i, j in Apos:
            self.Select(i, j, COLOR_CAPTURE)
        return True

    def Move(self, r0: int, c0: int, r1: int, c1: int):
        """Moves the piece if there. Handles capture, uncheck king and pawn promotion."""
        if (pid:=self.grid[r0, c0])==NULL and self.__status==IDLE and (r0, c0)==(r1, c1):
            return

        fr, en = self.TurnOf(), self.TurnOf(True)
        if en==(pid1:=self.grid[r1, c1])[0]: # KILL
            en.GetPiece(r1, c1, pid1[1]).alive = False
        
        if self.check: # UNCHECK KING
            loc = self.check.pieces[KING][0].loc
            self.board.cell(*loc).uncheck()

        # MOVE
        pc = fr.GetPiece(r0, c0)
        pc.move(r1, c1)
        self.grid[r1, c1] = pid
        self.board.move(r0, c0, r1, c1)
        del self.grid[r0, c0]

        if self.grid[r1, c1][1]==PAWN and pc.canmove is False: # PAWN PROMOTION
            self.paused = True
            self.board.AskPromotion(self.Promote, player=fr, pos=(r1,c1))


    def Select(self, r: int, c: int, fill_type: str):
        """Highlights the cell."""
        self.board.mark(r, c, fill_type)
        self.last_sel.append((r, c))

    def Deselect(self, r: int= None, c: int= None, *, all: bool = False):
        """If all is true ignores r,c else simply deselects all."""
        if all:
            for loc in self.last_sel:
                self.board.cell(*loc).deselect()
            self.last_sel.clear()
        else:
            self.board.cell(r, c).deselect()

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


    def Promote(self, *, player: Player, rank: str, pos: tuple[int]):
        """Promoting function. To be called by board after receiving Input."""
        r, c = pos
        pid = get_pid(player.name, rank)
        player.Promote(*pos, rank)
        self.board.cell(*pos).newimg(self.img[player.name, rank], pid)
        self.grid[r, c] = pid
        self.paused = False


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
    
    def PreFetchMoves(self) -> bool:
        """stores the moves and returns bool value if there is no move to move"""
        res = False
        pl = self.TurnOf()
        self.__moves.clear()

        for pcs in pl.pieces.values():
            for pc in pcs:
                if pc.alive:
                    loc = pc.loc
                    e,a = self.FilterMoves(*(pc.moves(self.grid.grid)), loc)
                    self.__moves[loc] = (e,a)
                    res = e or a or res
        return not res
    
    def IsMatchEnd(self):
        """determines whether game should be running or stopped"""
        if self.PreFetchMoves(): # 0 moves
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

"""
CYCLE:

start
    resetting players pieces and assigning turn on the fly
    set grid, load pieces in gui and backend
    checking match end symptoms
    prefetchmoves with filter applied
    check

after move
    clicked gets called on fly
    move happens
        move conditions checked
        kill gets checked
        unchecks the king if happens
        actual move in gui and backend
        pawn promotion is check if pawn is moved
    cells unhighlights
    turns gets switched
    match end detection

"""