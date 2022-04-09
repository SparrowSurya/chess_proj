import tkinter as tk
from configs.gui import *

from gui.cell import Cell


class ChessBoard:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas

        self.__cells:list[list[Cell]] = []

        # self.size = CH_SQSIZE
        # self.sel1 = CH_SEL1
        # self.sel2 = CH_SEL2
        # self.col1 = CH_CELL_COL1
        # self.col2 = CH_CELL_COL2
        # self.col0 = CH_TILE_OUTLINE
        # self.kill = CH_KILL
        # self.check = CH_CHECK
    
        for i in range(8):
            tmp = []
            for j in range(8):
                cell = Cell(self.canvas, i, j, self.get_fill_col(i, j), self.get_edge_col(i, j))
                tmp.append(cell)
            self.__cells.append(tmp)
    
    @staticmethod
    def xy2rc(x_coord: int, y_coord: int):
        """coords to cell coords"""
        c, r = x_coord//CH_SQSIZE, y_coord//CH_SQSIZE
        if r in range(8) and c in range(8):
            return r, c
        else:
            return -1, -1
    
    @staticmethod
    def get_fill_col(r: int, c: int):
        return CH_CELL_COL1 if (r+c)%2 else CH_CELL_COL2
    
    @staticmethod
    def get_edge_col(r: int, c: int):
        return CH_CELL_EDGE1 if (r+c)%2 else CH_CELL_EDGE2
    
    def cell(self, r: int, c: int) -> Cell:
        """returns the cell at r, c"""
        try:
            if r in range(8) and c in range(8):
                return self.__cells[r][c]
            return None
        except:
            return None

    def mark(self, r: int, c: int, fill_color: str, edge_color: str) -> bool:
        """to change colour of a cell returns sucess as bool"""
        if r==-1 and c==-1:
            return False
        else:
            self.cell(r, c).select(fill_color, edge_color)
            return True
    
