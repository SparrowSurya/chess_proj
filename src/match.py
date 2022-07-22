from tkinter import Event

from src.chessboard import ChessBoard
from src.chessgrid import ChessGrid
from src.piece import Piece
from src.player import Player
from const import *
from lib.utils import *


class Match:
    def __init__(self, chessboard: ChessBoard, chessgrid: ChessGrid):
        self.board = chessboard
        self.grid = chessgrid
        
        self.p0 = Player(P0)
        self.p1 = Player(P1)

        self.__status: str = IDLE

        self.last_loc: list[int, int] = [-1, -1] # x, y
        self.last_sel: list[tuple[int, int]] = [] # [(rn, cn), ...]

        self.drag: bool = None
        self.check: Player = None
        self.sel_flag = 0 # -1: old selection | 1: new selection | 0: None

        self.__legal_moves: dict[tuple, tuple] = {} # (r, c) -> (moves, attacks)
    
    @property
    def status(self):
        return self.__status

    # @__status.setter
    # def __status(self, new: str):
    #     """For handelling interruption between the match."""
    #     # taking decision based on the __status

    def Start(self, setup: str = None, turn: bool = P1):
        """Start game with given arrangement. ifgame is already running then ignores."""
        if self.__status == PLAY: return
        self.grid.grid = setup if setup is not None else DEFAULT_GRID
        if turn==P1:
            self.p0.Reset(False) and self.p1.Reset(True)
        elif turn==P0:
            self.p0.Reset(True) and self.p1.Reset(False)
        else:
            raise Exception(
                "[Invalid Player name] \n",
                f"player name: {turn}"
            )

        itr = iter(self.grid)
        for r in range(8):
            for c in range(8):
                if (pid:=next(itr))!=NULL:
                    self.LoadPiece(r, c, *pid)

        self.__status = PLAY
        self.IsMatchEnd()
        self.Check(self.p0)
        print(self.grid)
    
    def LoadPiece(self, r: int, c: int, player: str, piece: str):
        """Loads the piece in player pieces."""
        pid = get_pid(player, piece)
        self.board.new_piece(r, c, pid)
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

    def Check(self, player: Player):
        """Checks the check on player's king and displays if there."""
        if self._IsCheck(player):
            print("[CHECK]")
            self.check = player
            self.board.check(*player.pieces[KING][0].pos)
            return True
        return False
    
    def Clicked(self, click_type: str, e: Event):
        """Takes Click decision."""
        if self.__status is IDLE or self.__status is PAUSE: return

        if click_type=='<SLC>' and self.board.xy2rc(e.x, e.y) is not None:
            self._SLC(e.x, e.y)
        elif click_type=='<LD>':
            self._LD(e.x, e.y)
        elif click_type=='<LCR>':
            self._LCR(e.x, e.y)
        elif click_type=='<SRC>':
            self._SRC(e.x, e.y)
    
    def _SLC(self, x: int, y: int):
        """Underlying function for mouse single left click."""
        self.last_loc = [x, y]
        r, c = self.board.xy2rc(x, y)
        if self.last_sel:
            self.sel_flag = -1
            if (r,c) in self.last_sel[1:]: # clicked piece destination
                self.Move(*self.last_sel[0], r, c)
                self.Deselect(all=True)
                self.SwitchTurn()
                self.IsMatchEnd()
            elif (r, c) == self.last_sel[0]: # clicked at same piece
                self.MakeSelections(r, c)
                self.sel_flag = 1
            elif self.grid[r, c][0]==self.TurnOf(): # clicked another piece of same player
                self.MakeSelections(r, c)
                self.sel_flag = 1
            else: # clicked enemy piece
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
            self.board.drag(*pos, x-x1, y-y1)
        elif self.drag is None:
            pos = self.board.xy2rc(*self.last_loc)
            if pos in self.last_sel:
                cell = self.board._cell(*pos)
                ix, iy = cell.im_coord
                cell.drag(x-ix, y-iy)
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
                self.board.drag_reset(r0, c0)
                return
            else:
                r1, c1 = pos

            _mv = self.__legal_moves[(r0, c0)]
            if ((r1, c1) in _mv[0] or (r1, c1) in _mv[1]) and (r0, c0)!=(r1, c1):
                self.Move(r0, c0, r1, c1)
                self.Deselect(all=True)
                self.SwitchTurn()
                self.IsMatchEnd()
            else:
                self.board.drag_reset(r0, c0)
                self.Deselect(all=True)

        elif self.drag is None and self.sel_flag == -1:
            self.Deselect(all=True)

    def _SRC(self, x: int, y: int):
        """Underlying function for mouse right click."""
        self.Deselect(all=True)
        
    def MakeSelections(self, r: int, c: int):
        if self.grid[r, c] == NULL: return False
        self.Deselect(all=True)
        Epos, Apos, Spos = self.__legal_moves[(r, c)]
        self.Select(r, c)
        for i, j in Epos:
            self.Highlight(i, j)
        for i, j in Apos:
            self.UnderCapture(i, j)
        for i, j in Spos:
            self.Highlight(i, j, special=True)
        return True

    def Move(self, r0: int, c0: int, r1: int, c1: int):
        """Moves the piece if there. Handles capture, uncheck king, pawn promotion and checks whether acheck is given."""
        if (pid:=self.grid[r0, c0])==NULL or self.__status==IDLE or (r0, c0)==(r1, c1) or not (fr:=self.TurnOf()).IsOwner(pid):
            return

        en = self.TurnOf(True)
        pc = fr.GetPiece(r0, c0)
        if en==(pid1:=self.grid[r1, c1])[0]: # KILL
            en.GetPiece(r1, c1, pid1[1]).kill()
        
        if self.check: # UNCHECK KING
            self.board.uncheck()
            self.check = None

        # CASTELLING
        if (
            (r1, c1) in self.__legal_moves[(r0, c0)][2]
            and (r1==r0==0 or r1==r0==7)
            and pc.piece == KING
        ):
            if c1<c0:
                self.grid[r0, c0-1] = self.grid[r0, c0-4]
                self.board.move(r0, c0-4, r0, c0-1)
                fr.MovePiece(r0, c0+3, r0, c0-1)
                del self.grid[r0, c0-4]
            else:
                self.grid[r0, c0+1] = self.grid[r0, c0+3]
                self.board.move(r0, c0+3, r0, c0+1)
                fr.MovePiece(r0, c0+3, r0, c0+1)
                del self.grid[r0, c0+3]

        if (r1, c1) in self.__legal_moves[(r0, c0)][2] and pc.piece == PAWN: # EN PASSON
            en.GetPiece(r1-pc.step, c1, PAWN).kill()
            del self.grid[r1-pc.step, c1]
            self.board._cell(r1-pc.step, c1).clear_img()

        # MOVE
        fr.MovePiece(r0, c0, r1, c1)
        self.grid[r1, c1] = pid
        self.board.move(r0, c0, r1, c1)
        del self.grid[r0, c0]

        if pc.piece==PAWN and pc.r+pc.step not in range(8): # PAWN PROMOTION
            print("[PROMOTION]")
            self.board.AskPromotion(self._Promote, player=fr, pos=(r1,c1))
            self.__status = PAUSE
        self.Check(en)

    def Select(self, r: int, c: int):
        """Select the cell."""
        self.board.select(r, c)
        self.last_sel.append((r, c))

    def Highlight(self, r: int, c: int, *, special: bool = False):
        """Highlights the cell."""
        if special:
            self.board.special_highlight(r, c)
        else:
            self.board.highlight(r, c)
        self.last_sel.append((r, c))
        
    def UnderCapture(self, r: int, c: int):
        """Marks the cell piece under risk of capture."""
        self.board.underattack(r, c)
        self.last_sel.append((r, c))

    def Deselect(self, r: int= None, c: int= None, *, all: bool = False):
        """If all is true ignores r,c else simply deselects all."""
        if all:
            for loc in self.last_sel:
                self.board.deselect(*loc)
            self.last_sel.clear()
        else:
            self.board.deselect(r, c)

    def _IsCheck(self, player: Player, *, move: tuple = None, i: int = 0):
        """checks the Check on player's king
        move: [r0, c0, r1, c1] moves the piece(temporary)
        :i is used to get the king if player has more than one king"""
        r, c = player.pieces[KING][i].pos

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
            if (i:=r+dr) in range(8) and (j:=c+dc) in range(8):
                pid = grid[i][j]
                if pid!=NULL and pid[1]==KING and (not player.IsOwner(pid)):
                    return True
        
        for dr, dc in MARCH[KNIGHT]: # knight
            if (i:=r+dr) in range(8) and (j:=c+dc) in range(8):
                pid = grid[i][j]
                if pid!=NULL and pid[1]==KNIGHT and (not player.IsOwner(pid)):
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


    def _Promote(self, *, player: Player, rank: str, pos: tuple[int]):
        """Promoting function. To be called by board after receiving Input."""
        r, c = pos
        pid = get_pid(player.name, rank)
        player.Promote(*pos, rank)
        self.board.promote(*pos, pid)
        self.grid[r, c] = pid
        self.__status = PLAY

    def _FilterMoves(self, Epos, Apos, Ipos):
        """filters the move: Epos-empty, Apos-attack, Ipos-initial"""
        Fpos = [[], []]
        for i, pos in enumerate((Epos, Apos)):
            for r, c in pos:
                if self._IsCheck(self.TurnOf(), move=(*Ipos, r, c)):
                    continue
                else:
                    Fpos[i].append((r, c))
        return Fpos
    
    def _PreFetchMoves(self) -> bool:
        """stores the moves and returns bool value if there is no move to move"""
        res = False
        pl = self.TurnOf()
        self.__legal_moves.clear()

        for pcs in pl.pieces.values():
            for pc in pcs:
                if pc.alive:
                    e, a, s = self.PieceMoves(pc)
                    e,a = self._FilterMoves(e, a, pc.pos)
                    self.__legal_moves[pc.pos] = (e, a, s)
                    res = e or a or res
        return not res
    
    def IsMatchEnd(self):
        """Determines whether game should be running or stopped. Also pre fetches the moves."""
        if self._PreFetchMoves(): # 0 moves to play
            if self.check == self.TurnOf(): # since check for opponent king is calculated as soon move is done
                print("[MATCH ENDED]:- CHECKMATE")
            else:
                print("[MATCH ENDED]:- STALEMATE")
            return

        fr, en = self.TurnOf(), self.TurnOf(True)
        fd, ed = fr.alives, en.alives
        __stat = { KING: [0, 0], QUEEN: [0, 0], BISHOP: [0, 0], KNIGHT: [0, 0], ROOK: [0, 0], PAWN: [0, 0]} # [fr, en]

        for row in self.grid.grid:
            for (pl, pc) in row:
                if pl == pc: continue # to prevent NULL
                if pl is fr:
                    __stat[pc][0] += 1
                else:
                    __stat[pc][1] += 1

        # special cases
        if fd == ed == 1:
            print("[MATCH ENDED]:- king vs king")
        

    def march(self, grid: list[list[str]], r0: int, c0: int, dr: int, dc: int):
        """Marches given piece at r0,c0 wrt to dr,dc.
        Returns tuple[Empty positios in the way] and also returns tuple[r,c] if the next cell contained enemy piece."""
        if grid[r0][c0] == NULL:
            raise Exception(
                "[NO PIECE FOUND]",
                f"position: {r0, c0}"
            )

        r, c = r0+dr, c0+dc
        way = []
        while (r in range(8) and c in range(8)):
            pid = grid[r][c]
            if pid == NULL: # empty
                way.append((r, c))
            elif pid[0] == grid[r0][c0][0]: # friend
                return way, []
            else: # enemy
                return way, [(r, c)]
            r, c = r+dr, c+dc
        return way, []
    
    def PieceMoves(self, piece: Piece, *, grid:list[list[str]]=None):
        """Returns piece Empty pos and Attack pos and Special pos."""
        Epos, Apos, Spos = [], [], []
        grid = self.grid.grid if grid is None else grid
        player = self.TurnOf()
        if not player.IsOwner(piece.__call__()):
            player = self.TurnOf(True)

        if piece.piece==KING:
            for dr, dc in MARCH[KING]:
                r, c = piece.r+dr, piece.c+dc
                if r not in range(8) or c not in range(8): continue

                pid = grid[r][c]
                if pid == NULL: # empty
                    Epos.append((r, c))
                elif pid[0] == player: # friend
                    continue
                else: # enemy
                    Apos.append((r, c))

            # CASTELLING
            if piece.move0:
                r, c = piece.pos
                _rook_pidl, _rook_pidr = grid[r][c-4], grid[r][c+3]

                if (_rook_pidr[1] is ROOK
                    and player.GetPiece(r, c+3, ROOK).move0
                    and player.IsOwner(_rook_pidr)
                    and grid[r][c+1]==NULL
                    and grid[r][c+2]==NULL
                    and (not self._IsCheck(player, move=(r, c, r, c+2)))
                    and (not self._IsCheck(player, move=(r, c, r, c+1)))
                    ): Spos.append((r, c+2))

                if (_rook_pidl[1] is ROOK
                    and player.GetPiece(r, c-4, ROOK).move0
                    and player.IsOwner(_rook_pidl)
                    and grid[r][c-1]==NULL
                    and grid[r][c-2]==NULL
                    and grid[r][c-3]==NULL
                    and (not self._IsCheck(player, move=(r, c, r, c-2)))
                    and (not self._IsCheck(player, move=(r, c, r, c-1)))
                    ): Spos.append((r, c-2))

            return Epos, Apos, Spos

        elif piece.piece==QUEEN:
            for dr, dc in MARCH[QUEEN]:
                e, a = self.march(grid, piece.r, piece.c, dr, dc)
                Epos.extend(e)
                Apos.extend(a)
            return Epos, Apos, Spos

        elif piece.piece==KNIGHT:
            for dr, dc in MARCH[KNIGHT]:
                r, c = piece.r+dr, piece.c+dc
                if r not in range(8) or c not in range(8): continue

                pid = grid[r][c]
                if pid == NULL: # empty
                    Epos.append((r, c))
                elif pid[0] == player: # friend
                    continue
                else: # enemy
                    Apos.append((r, c))
            return Epos, Apos, Spos

        elif piece.piece==BISHOP:
            for dr, dc in MARCH[BISHOP]:
                e, a = self.march(grid, piece.r, piece.c, dr, dc)
                Epos.extend(e)
                Apos.extend(a)
            return Epos, Apos, Spos

        elif piece.piece==ROOK:
            for dr, dc in MARCH[ROOK]:
                e, a = self.march(grid, piece.r, piece.c, dr, dc)
                Epos.extend(e)
                Apos.extend(a)
            return Epos, Apos, Spos


        elif piece.piece==PAWN:
            r = piece.r + piece.step

            if grid[r][piece.c] == NULL: # step 1
                if r+piece.step in range(8):
                    Epos.append((r, piece.c))
                else: # one step before pawn promotion
                    Spos.append((r, piece.c))
                
            if (c:=piece.c+1) in range(8): # right enemy
                if (pid:=grid[r][c])[0] != player and pid != NULL:
                    Apos.append((r, c))
                    
            if (c:=piece.c-1) in range(8): # left enemy
                if (pid:=grid[r][c])[0] != player and pid != NULL:
                    Apos.append((r, c))
                    
            if piece.move0 and Epos:
                if r+piece.step in range(8) and grid[r+piece.step][piece.c] == NULL: # step 2
                    Epos.append((r+piece.step, piece.c))
            
            # EN PASSON
            if piece.r==4 and piece.step==1: k=2
            elif piece.r==3 and piece.step==-1: k=-2
            else: return Epos, Apos, Spos

            for d in (-1, 1):
                if (piece.c+d) not in range(8): continue
                _pid = self.grid[piece.r, piece.c+d]
                if (not player.IsOwner(_pid)
                    and _pid[1]==PAWN
                    and self.TurnOf(True).last_move == [piece.r+k, piece.c+d, piece.r, piece.c+d]
                    and not self._IsCheck(player, move=(piece.r, piece.c, piece.r+piece.step, piece.c+d))
                ):
                    Spos.append((piece.r+piece.step, piece.c+d))
            return Epos, Apos, Spos

''''
class Manager:

    def __init__(chessboard, chessgrid):
        self.board: ChessBoard
        self.grid :ChessGrid
        self.mode : PLAY/PAUSE/IDLE/EDIT

        self.last_loc: list[int x, int y]
        self.last_sel: list[tuple[int r, int c]]

        self.drag: bool
        self.check : None/Player
        self.sel_flag: -1/0/1

        self.__legal_moves: list[
            Epos: list[tuple[int r, int c]]
            Apos: list[tuple[int r, int c]]
            Spos: list[tuple[int r, int c]]
        ]

    def StartMatch(grid, turn: P0/P1):



'''