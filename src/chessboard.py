import tkinter as tk

from config import *
from const import *
from src.cell import Cell
from src.img import Image
from lib.utils import check_pid
from lib.graphics import ToImageTk, CheckerPattern


class ChessBoard:

    def __init__(self, master:tk.Frame, config: cfg, image_dict: Image):
        self.master: tk.Frame = master
        self.cfg: cfg = config
        self.img: Image = image_dict

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

        self.board = ToImageTk(CheckerPattern(CELLSIZE, self.cfg[COLOR_C1], self.cfg[COLOR_C2]))
        self.canvas.create_image(BORDER_WIDTH//2, BORDER_WIDTH//2, anchor=tk.NW, image=self.board)

        self.__cells = [
            [Cell(self.canvas, self.cfg, _i, _j) for _j in range(8)] for _i in range(8)
        ]
        self.canvas.tag_lower(self.board)

        # self.shade = ToImageTk(CircularGradient(CELLSIZE*8, CELLSIZE*8, ("#000000", "#330066"), (0, 1)))
        # self.screen = self.board.create_image(
        #     0, 0,
        #     image=self.shade,
        #     anchor=tk.NW,
        #     state=tk.HIDDEN
        # )


    def xy2rc(self, x_coord: int, y_coord: int, *, err: bool = False) -> tuple[int, int]:
        """Coords(x,y) to cell coords(r,c)if fails raises error"""
        c, r = (x_coord-BORDER_WIDTH//2)//CELLSIZE, (y_coord-BORDER_WIDTH//2)//CELLSIZE
        if r in range(8) and c in range(8):
            return r, c
        elif err:
            raise Exception(
                "[Invalid coordinates] \n", 
                f"no cell exists at that given coordinates:({x_coord}, {y_coord})"
            )
    
    def rc2xy(self, r: int, c: int) -> tuple[int, int]:
        """Returns x, y top left coordinate."""
        return c*CELLSIZE + BORDER_WIDTH//2, r*CELLSIZE + BORDER_WIDTH//2
    
    def _cell(self, r: int, c: int) -> Cell:
        """returns the cell at (r, c)."""
        try: return self.__cells[r][c]
        except IndexError: return
    
    def new_piece(self, r: int, c: int, pid: str):
        """Places new piece on board."""
        check_pid(pid)
        self._cell(r, c).new_img(self.img[pid], pid)

    def select(self, r: int, c: int):
        """Select the cell."""
        self._cell(r, c).select(COLOR_SELECT)
    
    def underattack(self, r: int, c: int):
        """Marks the piece under capture."""
        self._cell(r, c).select(COLOR_CAPTURE)
    
    def check(self, r: int, c: int):
        """Marks the piece under check."""
        self._cell(r, c).check()
    
    def uncheck(self, r: int, c: int):
        """Removes the piece under check."""
        self._cell(r, c).uncheck()

    def deselect(self, r: int, c: int):
        """Deselect the cell."""
        self._cell(r, c).deselect()

    def highlight(self, r: int, c: int):
        """Highlight the cell."""
        self._cell(r, c).select(self.cfg.highlight_type(r, c))

    def drag(self, r: int, c: int, dx: int, dy: int):
        """Drag move the image."""
        self._cell(r, c).drag(dx, dy)
    
    def drag_reset(self, r: int, c: int):
        """Reset the image location."""
        self._cell(r, c).reset_drag()
    
    def move(self, r0: int, c0: int, r1: int, c1: int):
        """Moves the image at cell (r0, c0) to cell(r1, c1)."""
        cell0 = self._cell(r0, c0)
        self._cell(r1, c1).new_img(self.img[cell0.pid], cell0.pid)
        cell0.clear_img()

    def promote(self, r: int, c: int, pid: str):
        """Changes the cell image to given pid."""
        self._cell(r, c).new_img(self.img[pid], pid)

    # def AskPromotion(self, func, **kwargs):
    #     """Special method to ask for pawn promotion."""
    #     # new method for selection will be implemented
        
    #     wd = ht = CELLSIZE*8
    #     ranks = {'queen': QUEEN, 'knight': KNIGHT, 'bishop': BISHOP, 'rook': ROOK}
    #     _rank = []

    #     def cmd():
    #         print(rank_var.get())
    #         select_bt.destroy()
    #         self.board.itemconfig(self.screen, state=tk.HIDDEN)
    #         func(**kwargs, rank=QUEEN)
    #         return
        
    #     rank_var = tk.StringVar()
    #     rank_var.set('queen')

    #     for i, k in enumerate(ranks.keys()):
    #         rb = tk.Radiobutton(self.board, name=k, value=k.capitalize(), variable=rank_var)
    #         rb.place(x=int(wd*0.4), y=int(ht*0.4) + 30*i)
    #         val = self.board.create_text(int(wd*0.5), int(ht*0.4) + 30*i, text=k.capitalize(), anchor=tk.N)
    #         self.board.tag_raise(val)
    #         _rank.append((rb, val))
        
    #     self.board.tag_raise(self.screen)
    #     self.board.itemconfig(self.screen, state=tk.NORMAL)
    #     # self.board.crea
    #     select_bt = ttk.Button(self.board, text='Select', command=cmd)
    #     select_bt.place(x=wd/2, y=int(ht*0.8), anchor=tk.S)
