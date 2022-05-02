import tkinter as tk

from gui.chessboard import ChessBoard
import config as cfg
from src.player import Player


class ctx:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board

        self.last_selected_cell = [] 
        self.last_clicked_loc = []
    
    def __select__(self, r: int, c: int, fill: str):
        """selects the given location"""
        self.board.mark(r, c, fill)
        self.last_selected_cell.append((r, c))
    
    def __deselect__(self, r: int, c: int):
        """deselects the given location"""
        self.board.cell(r, c).deselect()
    
    def deselect_all(self):
        """deselects all the selected cells"""
        for loc in self.last_selected_cell:
            self.__deselect__(*loc)
        self.last_selected_cell.clear()

    def single_left_click_only(self, e: tk.Event):
        self.deselect_all()

        if e.widget==self.board.board:
            self.last_clicked_loc.append((e.x, e.y))
            r, c = self.board.xy2rc(e.x, e.y)
            return self.__select__(r, c, cfg.CELL_SEL0)
    
    def single_right_click_only(self, e: tk.Event):
        self.deselect_all()


class Brain:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board
        self.ctx: ctx = ctx(self.board)
    
        self.__grid: list[list[str]] = []
        
        self.player0: Player = Player(self.board, cfg._Ref.p0)
        self.player1: Player = Player(self.board, cfg._Ref.p1)
    
    @property
    def grid(self):
        return self.__grid
    
    @grid.setter
    def grid(self, newgrid: list[list[str]]):
        self.__grid = newgrid
    
    