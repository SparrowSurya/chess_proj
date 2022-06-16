import tkinter as tk

import config as cfg
import config.const as const
from gui.cell import Cell
from utils.graphics import *


class ChessBoard:
    __slots__ = ('canvas', '__cells', 'board', 'temp', 'img')

    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas

        self.__cells:list[list[Cell]] = []

        # horizontal marking
        for i in range(8):
            x = cfg.BOARD_BORDER//2 + (cfg.SQSIZE)*i + cfg.SQSIZE//2
            y = cfg.BOARD_BORDER//4
            self.canvas.create_text(
                x,y, anchor=tk.CENTER, fill='white',
                text=const.MARKING[1][i],
                font=cfg.MARKING_FONT
            )
            self.canvas.create_text(
                x, 3*y+cfg.SQSIZE*8, anchor=tk.CENTER, fill='white',
                text=const.MARKING[1][i],
                font=cfg.MARKING_FONT
            )

        # vertical marking
        for i in range(8):
            x = cfg.BOARD_BORDER//4
            y = cfg.BOARD_BORDER//2 + (cfg.SQSIZE)*i + cfg.SQSIZE//2
            self.canvas.create_text(
                x, y, anchor=tk.CENTER, fill='white',
                text=const.MARKING[0][i],
                font=cfg.MARKING_FONT
            )
            self.canvas.create_text(
                3*x+cfg.SQSIZE*8, y, anchor=tk.CENTER, fill='white',
                text=const.MARKING[0][i],
                font=cfg.MARKING_FONT
            )
    
        self.board: tk.Canvas = tk.Canvas(self.canvas, height=cfg.SQSIZE*8, width=cfg.SQSIZE*8, highlightthickness=0)
        self.board.place(x=cfg.BOARD_BORDER//2, y=cfg.BOARD_BORDER//2)

        for y in range(8):
            tmp = []
            for x in range(8):
                cell = Cell(self.board, y, x, self.get_fill_col(y, x))
                tmp.append(cell)
            self.__cells.append(tmp)

        
        # wd = ht = cfg.SQSIZE*8
        # self.img = ToImageTk(FlatRectangle(wd, ht, "#FF00FF", 1))
                
        # self.temp = self.board.create_image(
        #     self.board.winfo_rootx(),
        #     self.board.winfo_rooty(),
        #     image=self.img,
        #     anchor=tk.NW,
        #     state=tk.NORMAL
        # )
        # self.board.tag_raise(self.temp)
    
    @staticmethod
    def xy2rc(x_coord: int, y_coord: int):
        """coords(x,y) to cell coords(r,c)"""
        c, r = x_coord//cfg.SQSIZE, y_coord//cfg.SQSIZE
        if r in range(8) and c in range(8):
            return r, c
        else:
            return None
    
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
        """to change colour of a cell"""
        self.cell(r, c).select(fill_color)
    
    def move(self, r0: int, c0: int, r1: int, c1: int, pid: str):
        """to move piece image to another cell"""
        cell0 = self.cell(r0, c0)
        img = cell0.img
        cell0.clearimg()
        self.cell(r1, c1).newimg(img, pid)
    
    # special
    def AskPromotion(self, func, **kwargs):
        print("ASKING PROMOTION")
        wd = ht = cfg.SQSIZE*8
        print(wd, ht)
        
        def cmd():
            print('PROMOTING')
            self.board.delete(temp)
            btn.destroy()
            func(**kwargs, rank=const.QUEEN)
            return

        im = FlatRectangle(wd, ht, "#FF00FF", 1)
        im.save("temp.png")
        img = ToImageTk(im)
        
        temp = self.board.create_image(
            0,
            0,
            image=img,
            anchor=tk.NW,
            state=tk.NORMAL
        )
        self.board.tag_raise(temp)

        btn = tk.Button(self.board, text='press', command=cmd)
        btn.place(x=wd/2, y=ht/2)
