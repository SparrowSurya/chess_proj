import tkinter as tk
from config import cfg
from const import *


class Cell:
    def __init__(self, board: tk.Canvas, config: cfg, r: int, c: int):
        self.board = board
        self.cfg = config
        self.r = r
        self.c = c
        self.__pid = NULL
        # self.__dx: int = 0
        # self.__dy: int = 0

        x0, y0 = self.c*CELLSIZE + BORDER_WIDTH//2, self.r*CELLSIZE + BORDER_WIDTH//2 
        self._cell = self.board.create_rectangle(
            x0, y0, x0+CELLSIZE, y0+CELLSIZE,
            state=tk.HIDDEN,
            width=0
        )

        self._image = self.board.create_image(
            x0+CELLSIZE//2, y0+CELLSIZE//2, anchor=tk.CENTER, state=tk.HIDDEN, image=""
        )


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
        # dx, dy = dx//1, dy//1
        # self.__dx += dx
        # self.__dy += dy
        self.board.move(self._image, dx, dy)

    def reset_drag(self):
        """Clears delta translation of image."""
        # self.board.move(self._image, -self.__dx, -self.__dy)
        # self.__dx, self.__dy = 0, 0
        x0, y0 = self.board.coords(self._image)
        x1, y1 = self.c*CELLSIZE + CELLSIZE//2 + BORDER_WIDTH//2, self.r*CELLSIZE + CELLSIZE//2 + BORDER_WIDTH//2
        self.board.move(self._image, x0-x1, y0-y1)
    
    def new_img(self, new: tk.PhotoImage, pid: str):
        """To place new Image."""
        self.board.itemconfig(self._image, state=tk.NORMAL, image=new)
        self.__pid = pid
        
    def clear_img(self):
        """Removes the image."""
        self.board.itemconfig(self._image, state=tk.HIDDEN, image="")

