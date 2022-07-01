import tkinter as tk

from gui import GUI
from config.const import *
from gui.img import Image
from src.chessgrid import ChessGrid
from src.match import Match


class Game:

    def __init__(self):
        self.gui = GUI()
        self._guisetup()

        self.chessboard = ChessGrid()
        self.img = Image()
        self.match = Match(self.gui.chessboard, self.chessboard, self.img)
        self._bind()
    
    def _guisetup(self):
        """Setup method for gui"""
        self.file_menu = self.gui.NewMenu('File')
        self.file_menu.add_command(label='New')
        self.file_menu.add_command(label='Open')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Settings')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.gui.quit)

        self.options_menu = self.gui.NewMenu('Options')
        self.options_menu.add_command(label='Play', command=lambda: self.match.Start(DEFAULT_GRID))
    
    def _bind(self):
        """Bind gui mouse/keyboard actions."""
        self.gui.bind("<Button-1>", self.Mouse_SLC)
        # self.gui.chessboard.board.bind("<Button-1>", self.Mouse_SLC)
    
    def Mouse_SLC(self, e:tk.Event):
        """Handles mouse single left click."""
        if self.match.status is not IDLE and e.widget==self.gui.chessboard.board:
            self.match.Clicked('<SLC>', e.x, e.y)

    def Mouse_LD(self, e: tk.Event):
        """bind event for left click drag"""
        if self.match.status is not IDLE and e.widget==self.gui.chessboard:
            self.match.Clicked('<LD>', e.x, e.y)

    def Mouse_LCR(self, e: tk.Event):
        """bind event for mouse left click release"""
        if self.match.status is not IDLE and e.widget==self.gui.chessboard:
            self.match.Clicked('<LCR>', e.x, e.y)

    def Mouse_SRC(self, e: tk.Event):
        """bind event with single right click"""
        if self.match.status is not IDLE and e.widget==self.gui.chessboard:
            self.match.Clicked('<SRC>', e.x, e.y)


'''

    def __init__(self, display: tk.Frame, config: cfg):
        self.display: tk.Frame = display
        self.cfg: cfg = config

        self.board: ChessBoard = ChessBoard(self.display, self.cfg)
        self.img: Image = Image()
        self.grid: ChessGrid = ChessGrid()

        self.player0: Player = Player(self.board, P0)
        self.player1: Player = Player(self.board, P1)

        self.inMatch: bool = False
        self.paused: bool = False

        self.last_clicked: list[int] = [-1, -1] # [x, y]
        self.last_selected: list[tuple[int, int]] = [] # [(r0, c0), (r1, c1), ...]

        self.selected: int = 0 # 0-nothing; 1-active: -1:passive
        self.pdrag: bool  = None

        self.check: Player = None

        self.__moves: dict[tuple, tuple] = {} # to pre fetch moves (also used for cache and end game detection)

    def Mouse_SLC(self, e: tk.Event):
        """bind event with single left click"""
        if not self.inMatch or self.paused: return
        
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

                self.Select(*loc, self.cfg[ACTIVE])
                for i, j in Epos:
                    self.Select(i, j, self.cfg[COLOR_S1])
                for i, j in Apos:
                    self.Select(i, j, self.cfg[COLOR_CAPTURE])
                self.selected = 1

        else:
            if e.widget==self.board.board and self.grid[r, c][0]==self.TurnOf(): # HIGHLIGHT MOVES 
                loc = self.board.xy2rc(e.x, e.y)
                Epos, Apos = self.__moves[loc]

                self.Select(*loc, self.cfg[COLOR_S0])
                for i, j in Epos:
                    self.Select(i, j, self.cfg[COLOR_S1])
                for i, j in Apos:
                    self.Select(i, j, self.cfg[COLOR_CAPTURE])
                self.selected = 1
        self.pdrag = None

    def MouseDrag(self, e: tk.Event):
        """bind event for left click drag"""
        if not self.inMatch or self.paused: return
        
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
        if not self.inMatch or self.paused: return
        
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
        if not self.inMatch or self.paused: return
        
        self.DeselectAll()
'''