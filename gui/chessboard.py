import tkinter as tk

import config as cfg
import config.const as const
from gui.cell import Cell


class ChessBoard:
    __slots__ = ('canvas', '__cells', 'board')

    def __init__(self, canvas:tk.Canvas):
        self.canvas = canvas

        self.__cells:list[list[Cell]] = []

        # horizontal marking
        for i in range(8):
            x = cfg.BOARD_BORDER//2 + (cfg.SQSIZE)*i + cfg.SQSIZE//2
            y = cfg.BOARD_BORDER//4
            canvas.create_text(
                x,y, anchor=tk.CENTER, fill='white',
                text=const.MARKING[1][i],
                font=cfg.MARKING_FONT
            )
            canvas.create_text(
                x, 3*y+cfg.SQSIZE*8, anchor=tk.CENTER, fill='white',
                text=const.MARKING[1][i],
                font=cfg.MARKING_FONT
            )

        # vertical marking
        for i in range(8):
            x = cfg.BOARD_BORDER//4
            y = cfg.BOARD_BORDER//2 + (cfg.SQSIZE)*i + cfg.SQSIZE//2
            canvas.create_text(
                x, y, anchor=tk.CENTER, fill='white',
                text=const.MARKING[0][i],
                font=cfg.MARKING_FONT
            )
            canvas.create_text(
                3*x+cfg.SQSIZE*8, y, anchor=tk.CENTER, fill='white',
                text=const.MARKING[0][i],
                font=cfg.MARKING_FONT
            )
    
        self.board: tk.Canvas = tk.Canvas(canvas, height=cfg.SQSIZE*8, width=cfg.SQSIZE*8, highlightthickness=0)
        self.board.place(x=cfg.BOARD_BORDER//2, y=cfg.BOARD_BORDER//2)

        for y in range(8):
            tmp = []
            for x in range(8):
                cell = Cell(self.board, y, x, self.get_fill_col(y, x))
                tmp.append(cell)
            self.__cells.append(tmp)
    
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
        func(**kwargs, rank=const.QUEEN) # temporary
        return
        print("ASKING PROMOTION")
        temp = tk.Frame(self.board, bg='yellow', width=self.canvas.winfo_width(), height=self.canvas.winfo_height())
        temp.place(x=self.canvas.winfo_rootx(), y=self.canvas.winfo_rooty())
        
        def cmd():
            print('PROMOTING')
            func(**kwargs, rank=const.QUEEN)
            temp.destroy()
            return

        tk.Button(temp, text='press', command=cmd).pack()

