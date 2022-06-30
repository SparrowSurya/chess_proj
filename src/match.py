from collections import namedtuple

from gui.img import Image
from gui.chessboard import ChessBoard
from src.chessgrid import ChessGrid
from src.player import Player
from config.const import *
from lib.utils import *

class Match:

    def __init__(self, chessboard: ChessBoard, chessgrid: ChessGrid, image_dict: Image):
        self.Board = chessboard
        self.Grid = chessgrid
        self.Img = image_dict
        
        self.p0: Player = Player(P0)
        self.p1: Player = Player(P1)

        self.__status: str = IDLE

        self.last_loc: list[int, int] = [-1, -1] # x, y
        self.last_sel: list[tuple[int, int]] = [] # [(rn, cn), ...]

        self.drag: bool = None
        self.check: Player = None

        self.__moves: dict[tuple, tuple] = {} # piece_pos -> (moves, attacks)


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
        self.Grid.grid = setup if setup is not None else DEFAULT_GRID
        itr = iter(self.Grid)
        for r in range(8):
            for c in range(8):
                pid = next(itr)
                if pid!=NULL: self.Board.cell(r, c).newimg(self.Img[pid], pid)
        self.p1.turn = True
        self.p0.turn = False
        self.__status = PLAY
        self.PreFetchMoves()
    
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
            (pl:=self.p1).turn = True
        else:
            (pl:=self.p0).turn = True
            self.p1.turn = False

        print(self.Grid)
        if self.IsCheck(pl):
            self.check = pl
            pc = pl.pieces[KING][0]
            self.Board.cell(*(pc.loc)).select(self.Board.cfg[COLOR_CHECK])

    def Move(self, r0: int, c0: int, r1: int, c1: int):
        """Moves the piece if there. Handles capture, uncheck king and pawn promotion."""
        if (pid:=self.Grid[r0, c0])!=NULL and self.__status==PLAY:
            return

        fr, en = self.TurnOf(), self.TurnOf(True)

        if en==(pid1:=self.Grid[r1, c1])[0]: # KILL
            en.GetPiece(r1, c1, pid1[1]).alive = False
        
        if self.check: # UNCHECK KING
            loc = self.check.pieces[KING][0].loc
            self.Board.cell(*loc).uncheck()

        pc = fr.GetPiece(r0, c0)
        pc.move(r1, c1)
        self.Grid[r1, c1] = pid
        del self.Grid[r0, c0]

        if self.Grid[r1, c1][1]==PAWN and pc.canmove is False: # PAWN PROMOTION
            self.paused = True
            self.Board.AskPromotion(self.Promote, player=fr, pos=(r1,c1))


    def Select(self, r: int, c: int, fill_type: str):
        """Highlights the cell."""
        self.Board.mark(r, c, fill_type)

    def Deselect(self, r: int= None, c: int= None, *, all: bool = False):
        """If all is true ignores r,c else simply deselects all."""
        if all:
            for loc in self.last_sel:
                self.Board.cell(*loc).deselect()
            self.last_sel.clear()
        else:
            self.Board.cell(r, c).deselect()

    def IsCheck(self, player: Player, *, move: tuple = None, i: int = 0):
        """checks the Check on player's king
        move: [r0, c0, r1, c1] moves the piece(temporary)
        :i is used to get the king if player has more than one king"""
        r, c = player.pieces[KING][i].loc

        grid = self.Grid.grid
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
        self.Board.cell(*pos).newimg(self.Img[player.name, rank], pid)
        self.Grid[r, c] = pid
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
                    e,a = self.FilterMoves(*(pc.moves(self.Grid)), loc)
                    self.__moves[loc] = (e,a)
                    res = e or a or res
        return not res
    
    def EndMatch(self):
        """determines whether game should be running or stopped"""
        if self.PreFetchMoves(): # 0 moves
            print("[MATCH ENDED]:- no moves to play")
            return

        fr, en = self.TurnOf(), self.TurnOf(True)
        fd, ed = fr.alives, en.alives
        stat = { KING: [0, 0], QUEEN: [0, 0], BISHOP: [0, 0], KNIGHT: [0, 0], ROOK: [0, 0], PAWN: [0, 0]} # [fr, en]

        for row in self.Grid.grid:
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
