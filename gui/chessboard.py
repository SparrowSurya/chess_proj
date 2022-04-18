import tkinter as tk

import config as cfg
from gui.cell import Cell
import gui.ipath as im


class ChessBoard:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas

        self.__cells:list[list[Cell]] = []
    
        for i in range(8):
            tmp = []
            for j in range(8):
                cell = Cell(self.canvas, i, j, self.get_fill_col(i, j))
                tmp.append(cell)
            self.__cells.append(tmp)
    
    @staticmethod
    def xy2rc(x_coord: int, y_coord: int):
        """coords to cell coords"""
        c, r = x_coord//cfg.SQSIZE, y_coord//cfg.SQSIZE
        if r in range(8) and c in range(8):
            return r, c
        else:
            return -1, -1
    
    @staticmethod
    def get_fill_col(r: int, c: int):
        return cfg.CELL_COL1 if (r+c)%2 else cfg.CELL_COL2
        
    @staticmethod
    def get_sel_col(r: int, c: int):
        return cfg.CELL_SEL1 if (r+c)%2 else cfg.CELL_SEL2
    
    def cell(self, r: int, c: int) -> Cell:
        """returns the cell at r, c"""
        try:
            if r in range(8) and c in range(8):
                return self.__cells[r][c]
            return
        except:
            return

    def mark(self, r: int, c: int, fill_color: str) -> bool:
        """to change colour of a cell returns sucess as bool"""
        if r==-1 and c==-1:
            return False
        else:
            self.cell(r, c).select(fill_color)
            return True
    
