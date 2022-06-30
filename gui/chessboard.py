import tkinter as tk
from tkinter import ttk

from config import *
from gui.cell import Cell
from lib.graphics import ToImageTk, CircularGradient


class ChessBoard:

    def __init__(self, master:tk.Frame, config: cfg):
        self.master: tk.Frame = master
        self.cfg: cfg = config

        self.__cells:list[list[Cell]] = []

        self.canvas: tk.Canvas = tk.Canvas(
            self.master,
            bg='#7d4512',
            height= CELLSIZE*8 + BORDER_WIDTH,
            width= CELLSIZE*8 + BORDER_WIDTH,
            highlightthickness=0
        )

        # horizontal marking
        for i in range(8):
            x = BORDER_WIDTH//2 + CELLSIZE*i + CELLSIZE//2
            y = BORDER_WIDTH//4
            self.canvas.create_text(
                x,y, anchor=tk.CENTER, fill='white',
                text=MARKING[1][i],
                font=FONT_BORDER
            )
            self.canvas.create_text(
                x, 3*y+CELLSIZE*8, anchor=tk.CENTER, fill='white',
                text=MARKING[1][i],
                font=FONT_BORDER
            )

        # vertical marking
        for i in range(8):
            x = BORDER_WIDTH//4
            y = BORDER_WIDTH//2 + (CELLSIZE)*i + CELLSIZE//2
            self.canvas.create_text(
                x, y, anchor=tk.CENTER, fill='white',
                text=MARKING[0][i],
                font=FONT_BORDER
            )
            self.canvas.create_text(
                3*x+CELLSIZE*8, y, anchor=tk.CENTER, fill='white',
                text=MARKING[0][i],
                font=FONT_BORDER
            )
    
        self.board: tk.Canvas = tk.Canvas(self.canvas, height=CELLSIZE*8, width=CELLSIZE*8, highlightthickness=0)
        self.board.place(x=BORDER_WIDTH//2, y=BORDER_WIDTH//2)

        for y in range(8):
            tmp = []
            for x in range(8):
                cell = Cell(self.board, self.cfg, y, x, self.get_fill_col(y, x))
                tmp.append(cell)
            self.__cells.append(tmp)

        self.shade = ToImageTk(CircularGradient(CELLSIZE*8, CELLSIZE*8, ("#000000", "#330066"), (0, 1)))
        self.screen = self.board.create_image(
            0, 0,
            image=self.shade,
            anchor=tk.NW,
            state=tk.HIDDEN
        )


    def xy2rc(self, x_coord: int, y_coord: int):
        """Coords(x,y) to cell coords(r,c)if fails raises error"""
        c, r = x_coord//CELLSIZE, y_coord//CELLSIZE
        if r in range(8) and c in range(8):
            return r, c
        else:
            raise Exception(
                "[Invalid coordinates] \n", 
                f"no cell exists at that given coordinates:({x_coord}, {y_coord})"
            )

    def get_fill_col(self, r: int, c: int):
        """Returns cell colour based on its location."""
        return self.cfg[COLOR_C1] if (r+c)%2 else self.cfg[COLOR_C2]
    
    def cell(self, r: int, c: int) -> Cell:
        """returns the cell at (r, c)."""
        try:
            if r in range(8) and c in range(8):
                return self.__cells[r][c]
            return
        except:
            return

    def mark(self, r: int, c: int, fill_type: str) -> bool:
        """Changes colour of a cell at (r, c).
        parameter fill_type is the type of mark."""
        self.cell(r, c).select(fill_type)
    
    def move(self, r0: int, c0: int, r1: int, c1: int, pid: str):
        """Moves the image at cell (r0, c0) to cell(r1, c1)."""
        cell0 = self.cell(r0, c0)
        img = cell0.img
        cell0.clear_img()
        self.cell(r1, c1).newimg(img, pid)
    
    def AskPromotion(self, func, **kwargs):
        """Special method to ask for pawn promotion."""
        # new method for selection will be implemented
        
        wd = ht = CELLSIZE*8
        ranks = {'queen': QUEEN, 'knight': KNIGHT, 'bishop': BISHOP, 'rook': ROOK}
        _rank = []

        def cmd():
            print(rank_var.get())
            select_bt.destroy()
            self.board.itemconfig(self.screen, state=tk.HIDDEN)
            func(**kwargs, rank=QUEEN)
            return
        
        rank_var = tk.StringVar()
        rank_var.set('queen')

        for i, k in enumerate(ranks.keys()):
            rb = tk.Radiobutton(self.board, name=k, value=k.capitalize(), variable=rank_var)
            rb.place(x=int(wd*0.4), y=int(ht*0.4) + 30*i)
            val = self.board.create_text(int(wd*0.5), int(ht*0.4) + 30*i, text=k.capitalize(), anchor=tk.N)
            self.board.tag_raise(val)
            _rank.append((rb, val))
        
        self.board.tag_raise(self.screen)
        self.board.itemconfig(self.screen, state=tk.NORMAL)
        # self.board.crea
        select_bt = ttk.Button(self.board, text='Select', command=cmd)
        select_bt.place(x=wd/2, y=int(ht*0.8), anchor=tk.S)
