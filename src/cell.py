import tkinter as tk
from config import cfg
from const import *
from lib.graphics import ToImageTk, CircularGradient


class Cell:
    def __init__(self, board: tk.Canvas, config: cfg, r: int, c: int):
        self.board = board
        self.cfg = config
        self.r = r
        self.c = c

        x0, y0 = self.c*CELLSIZE + BORDER_WIDTH//2, self.r*CELLSIZE + BORDER_WIDTH//2 
        self._cell = self.board.create_rectangle(
            x0, y0, x0+CELLSIZE, y0+CELLSIZE,
            state=tk.HIDDEN,
            width=0
        )

        self._check_im = ToImageTk(CircularGradient(
            CELLSIZE, CELLSIZE, 
            (self.cfg[self.cfg.color_type(r,c)], self.cfg[COLOR_CHECK]),
            alpha=(0.4, 1),
        ))

        self._check = self.board.create_image(
            x0, y0, anchor=tk.NW, state=tk.HIDDEN, image=self._check_im
        )

        self._image = self.board.create_image(
            x0+CELLSIZE//2, y0+CELLSIZE//2, anchor=tk.CENTER, state=tk.HIDDEN, image=""
        )

        self.__pid = NULL
        self.__dx: int = 0
        self.__dy: int = 0

    @property
    def pid(self):
        return self.__pid
    
    @property
    def im_coord(self):
        return self.board.coords(self._image)
    
    @property
    def color(self):
        return self.board.itemcget(self._cell, 'fill')
    
    @property
    def state(self):
        return self.board.itemcget(self._cell, 'state')
    
    def check(self):
        """Shows check on it."""
        self.board.itemconfig(self._check, state=tk.NORMAL)
    
    def uncheck(self):
        """Removes check on it."""
        self.board.itemconfig(self._check, state=tk.HIDDEN)
    
    def select(self, mode: str):
        """Selectes the cell to selection mode."""
        self.board.itemconfig(self._cell, fill=self.cfg[mode], state=tk.NORMAL)
    
    def deselect(self):
        """Deselects the cell and removes visibility."""
        self.board.itemconfig(self._cell, fill="", state=tk.HIDDEN)

    def drag(self, dx: int, dy: int):
        """
        Changes the position of image on screen.
        Parameter should be relative to current location.
        Adds these coords to delta translation.
        """
        self.board.tag_raise(self._image)
        dx, dy = dx//1, dy//1
        self.__dx += dx
        self.__dy += dy
        self.board.move(self._image, dx, dy)

    def reset_drag(self):
        """Clears delta translation of image."""
        self.board.move(self._image, -self.__dx, -self.__dy)
        self.__dx = 0
        self.__dy = 0
    
    def new_img(self, new: tk.PhotoImage, pid: str):
        """To place new Image."""
        self.board.itemconfig(self._image, state=tk.NORMAL, image=new)
        self.__pid = pid
        
    def clear_img(self):
        """Removes the image."""
        self.board.itemconfig(self._image, state=tk.HIDDEN, image="")