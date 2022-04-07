import tkinter as tk
from configs.gui import *

from gui.cell import Cell

class ChessBoard:
    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas

        self.__cells:list[list[Cell]] = []

        self.cell_size = CH_SQSIZE
        self.sel1 = CH_SELECT_COL1
        self.sel2 = CH_SELECT_COL2
        self.col1 = CH_TILE_COL1
        self.col2 = CH_TILE_COL2
        self.col0 = CH_TILE_OUTLINE
        self.kill = CH_KILL
        self.check = CH_CHECK
    
    def cell(self, ix, iy):
        """returns the cell"""
        return self.__cells[iy][ix]

    def draw(self):
        """draws chessboard"""
        for i in range(8):
            tmp = []
            for j in range(8):
                col = self.col1 if (i+j)%2 else self.col2
                cell = Cell(self.canvas, i, j, self.cell_size, col, self.col0)
                tmp.append(cell)
            self.__cells.append(tmp)

    def select(self, x, y):
        self.__cells[y//self.cell_size][x//self.cell_size].select(self.sel1)
