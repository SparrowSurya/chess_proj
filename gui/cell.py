import tkinter as tk
from config import cfg
from config.const import *

class Cell:
    
    def __init__(self, board: tk.Canvas, config: cfg, row: int, column: int, fill: str, img=""):
        self.board: tk.Canvas = board
        self.cfg: cfg = config
        self.r: int = row
        self.c: int = column
        self.fill: str = fill
        self.img = img

        self.pid: str = NULL
        self.selected: bool = False
        self.highlighted: bool = False
        self.__dx: int = 0
        self.__dy: int = 0

        self.color = self.board.create_rectangle(
            self.c*CELLSIZE,
            self.r*CELLSIZE,
            (self.c+1)*CELLSIZE,
            (self.r+1)*CELLSIZE,
            fill=self.fill,
            width=0,
        )

        self.image = self.board.create_image(
            (2*self.c +1)*CELLSIZE //2,
            (2*self.r +1)*CELLSIZE //2,
            anchor=tk.CENTER,
            state=tk.HIDDEN,
            image=self.img
        )
    
    def select(self, color_type: str) -> str:
        """Selecting cell by colouring it. Check is a special case. Returns currently selected color."""
        if self.highlighted == self.cfg[COLOR_CHECK]:
            self.__Mark_cell(SELECT)
        else:
            self.__Mark_cell(color_type)
            self.board.tag_raise(self.image)
        self.selected = True
        return self.ACTIVE_COLOR
    
    def deselect(self):
        """Cell back to its original color. Check is a special case."""
        if self.highlighted:
            self.__Mark_cell(COLOR_CHECK)
        else:
            self.__Mark_cell(NORMAL)
        self.selected = False
    
    def check(self):
        """Marks cell as check."""
        if self.pid[1]==KING:
            self.__Mark_cell(COLOR_CHECK)
            self.highlighted = True
    
    def danger(self):
        """Marks cell as risk to be attacked."""
        if self.pid[1]!=KING:
            self.__Mark_cell(COLOR_CAPTURE)

    def uncheck(self):
        """To handle special case in select and deselect ie to remove check."""
        self.highlighted = False
        self.board.itemconfig(self.color, fill=self.fill)
    
    @property
    def ACTIVE_COLOR(self):
        """returns current colur being displayed"""
        return self.board.itemcget(self.color, 'fill')
    
    def newimg(self, image: tk.PhotoImage, pid: str):
        """Sets new image."""
        self.board.itemconfig(self.image, image=image, state=tk.NORMAL)
        self.img = image
        self.pid = pid
    
    def show_img(self):
        """Shows the image displayed."""
        self.__Img_state(tk.NORMAL)
        self.lift()
    
    def hide_img(self):
        """Hides the image displayed."""
        self.__Img_state(tk.HIDDEN)
    
    def clear_img(self):
        """Clears the image cell has currently."""
        self.board.itemconfig(self.image, image="")
        self.img = ""
        self.pid = NULL
    
    def move(self, dx: int, dy: int):
        """
        Changes the position of image on screen.
        Parameter should be relative to current location.
        Adds these coords to delta translation.
        """
        dx, dy = dx//1, dy//1
        self.__dx += dx
        self.__dy += dy
        self.board.move(self.image, dx, dy)
    
    @property
    def COORDs(self):
        """Returns the coordinates (row, column) of cell"""
        return self.r, self.c
    
    @property
    def COORDS_IMG(self):
        """returns image coordinates (Row, column)."""
        return self.board.coords(self.image)
    
    def reset_move(self):
        """Clears delta translation of image."""
        self.board.move(self.image, -self.__dx, -self.__dy)
        self.__dx = 0
        self.__dy = 0
    
    def lift(self):
        """To lift up image to top."""
        self.board.tag_raise(self.image)
    
    def __Mark_cell(self, color_type: str):
        """Changes the cell color. Is called by every cell status method"""
        if color_type is NORMAL:
            self.board.itemconfig(self.color, fill=self.fill)
        elif color_type is COLOR_CHECK:
            self.board.itemconfig(self.color, fill=self.cfg[color_type])
            self.highlighted = True
        else:
            self.board.itemconfig(self.color, fill=self.cfg[color_type])
    
    def __Img_state(self, state: str):
        """Changes state of cell image. Is called by every image state method"""
        self.board.itemconfig(self.image, state=state)

    def config(self, key: str, value: str, **kwargs):
        pass