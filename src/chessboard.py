import tkinter as tk

from config import *
from const import *
from src.cell import Cell
from src.img import Image
from lib.utils import check_pid
from lib.graphics import CircularGradient, ToImageTk, CheckerPattern


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

        self._board = ToImageTk(CheckerPattern(CELLSIZE, self.cfg[COLOR_C1], self.cfg[COLOR_C2]))
        self.canvas.create_image(BORDER_WIDTH//2, BORDER_WIDTH//2, anchor=tk.NW, image=self._board)

        self.__cells = [
            [Cell(self.canvas, self.cfg, _i, _j) for _j in range(8)] for _i in range(8)
        ]
        self.canvas.tag_lower(self._board)

        self._shade_im = ToImageTk(CircularGradient(CELLSIZE*8, CELLSIZE*8, ("#000000", "#F5F5F5"), (0.5, 1)))
        self._check_im = ToImageTk(CircularGradient(
            CELLSIZE, CELLSIZE, 
            ("#DDDDDD", self.cfg[COLOR_CHECK]),
            alpha=(0.4, 1),
        ))
        self._check = self.canvas.create_image(0, 0, anchor=tk.NW, image=self._check_im, state=tk.HIDDEN)


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
        """Returns x, y top left coordinate. Only for cell."""
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
        (xi, yi), (xf, yf) = self.canvas.coords(self._check), self.rc2xy(r, c)
        self.canvas.move(self._check, xf-xi, yf-yi)
        self.canvas.tag_raise(self._cell(r, c)._image, self._check)
        self.canvas.itemconfig(self._check, state=tk.NORMAL)

    def uncheck(self):
        """Removes the piece under check."""
        self.canvas.itemconfig(self._check, state=tk.HIDDEN)

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

    def AskPromotion(self, func, **kwargs):
        """Special method to ask for pawn promotion."""
        screen = self.canvas.create_image(BORDER_WIDTH//2, BORDER_WIDTH//2, anchor=tk.NW, image=self._shade_im)      
        (x0, y0), pl = self.rc2xy(*kwargs['pos']), kwargs['player']

        def cmd(rank):
            self.canvas.delete(box, queen, knight, bishop, rook, screen)
            func(rank=rank, **kwargs)

        if y0<self.canvas.winfo_height()//2:
            flow = 1
            y0 += CELLSIZE
            box = self.canvas.create_rectangle(x0, y0, x0+CELLSIZE, y0+CELLSIZE*4, fill=self.cfg[COLOR_SELECT], width=0)
        else:
            flow = -1
            box = self.canvas.create_rectangle(x0, y0-CELLSIZE*4, x0+CELLSIZE, y0, fill=self.cfg[COLOR_SELECT], width=0)

        queen = self.canvas.create_image(
            x0+CELLSIZE//2, y0+(CELLSIZE*flow)//2, anchor=tk.CENTER, image=self.img[f"{pl}{QUEEN}"])
        knight = self.canvas.create_image(
            x0+CELLSIZE//2, y0+(CELLSIZE*flow*3)//2, anchor=tk.CENTER, image=self.img[f"{pl}{KNIGHT}"])
        bishop = self.canvas.create_image(
            x0+CELLSIZE//2, y0+(CELLSIZE*flow*5)//2, anchor=tk.CENTER, image=self.img[f"{pl}{BISHOP}"])
        rook = self.canvas.create_image(
            x0+CELLSIZE//2, y0+(CELLSIZE*flow*7)//2, anchor=tk.CENTER, image=self.img[f"{pl}{ROOK}"])

        self.canvas.tag_bind(queen, '<Button-1>', lambda x: cmd(QUEEN))
        self.canvas.tag_bind(knight, '<Button-1>', lambda x: cmd(KNIGHT))
        self.canvas.tag_bind(bishop, '<Button-1>', lambda x: cmd(BISHOP))
        self.canvas.tag_bind(rook, '<Button-1>', lambda x: cmd(ROOK))