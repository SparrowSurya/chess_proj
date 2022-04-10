import tkinter as tk

# from configs.gui import *
import config
from gui.chessboard import ChessBoard


class ctxManager:
    def __init__(self, board: ChessBoard):
        self.board: ChessBoard = board

        self.last_selected_cell = [] 
        self.last_clicked_loc = []
    
    def __select__(self, r: int, c: int):
        """selects the given location"""
        f = self.board.get_fill_col(r,c+1)
        e = self.board.get_edge_col(r,c+1)
        self.board.mark(r, c, f, e)
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

        if e.widget==self.board.canvas:
            self.last_clicked_loc.append((e.x, e.y))
            return self.__select__(*self.board.xy2rc(e.x, e.y))
    
    def single_right_click_only(self, e: tk.Event):
        self.deselect_all()