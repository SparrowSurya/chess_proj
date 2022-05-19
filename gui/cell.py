import tkinter as tk
import config as cfg
from config.const import NULL

class Cell:
    __slots__ = ('canvas', 'ix', 'iy', 'pid', 'selected', 'fill', '__dx', '__dy', 'img', 'cell_col', 'cell_img')
    
    def __init__(self, canvas: tk.Canvas, row: int, column: int, fill: str, image=""):
        self.canvas: tk.Canvas = canvas
        self.ix: int = column
        self.iy: int = row
        self.pid: str = NULL
        self.selected: str = ''

        self.fill: str = fill

        self.__dx: int = 0
        self.__dy: int = 0
        
        self.img = image

        self.cell_col = self.canvas.create_rectangle(
            self.ix*cfg.SQSIZE,
            self.iy*cfg.SQSIZE,
            (self.ix+1)*cfg.SQSIZE,
            (self.iy+1)*cfg.SQSIZE,
            fill=self.fill,
            width=0,
        )

        self.cell_img = self.canvas.create_image(
            (2*self.ix +1)*cfg.SQSIZE //2,
            (2*self.iy +1)*cfg.SQSIZE //2,
            anchor=tk.CENTER,
            state=tk.NORMAL,
            image=self.img
        )
    
    def select(self, fill_color: str):
        """selecting cell by colouring it, CHECK is a special case"""
        if self.selected == cfg.CHECK:
            self.canvas.itemconfig(self.cell_col, fill=cfg.CELL_SEL0)
        else:
            self.canvas.itemconfig(self.cell_col, fill=fill_color)
            self.selected = fill_color
            self.canvas.tag_raise(self.cell_img)
    
    def deselect(self):
        """giving cell its original color, CHECK is a special case"""
        if self.selected == cfg.CHECK:
            self.canvas.itemconfig(self.cell_col, fill=cfg.CHECK)
        else:
            self.canvas.itemconfig(self.cell_col, fill=self.fill)
            self.selected = ''
        
    def uncheck(self):
        """to handle specific case in select and deselect"""
        self.selected = ''
        self.canvas.itemconfig(self.cell_col, fill=self.fill)
    
    def activecol(self):
        """returns current colur being displayed"""
        return self.canvas.itemcget(self.cell_col, 'fill')
    
    def newimg(self, image, pid):
        """give cell an piece image"""
        self.img = image
        self.pid = pid
        self.canvas.itemconfig(self.cell_img, image=self.img)
        self.canvas.tag_raise(self.cell_img)
    
    def showimg(self):
        """to show the image displayed by the cell"""
        self.canvas.itemconfig(self.cell_img, state=tk.NORMAL)
        self.canvas.tag_raise(self.cell_img)
    
    def hideimg(self):
        """to hide the image displayed by the cell"""
        self.canvas.itemconfig(self.cell_img, state=tk.HIDDEN)
    
    def clearimg(self):
        """remove the images"""
        self.canvas.itemconfig(self.cell_img, image="")
        self.img = ""
        self.pid = NULL
    
    def move(self, dx: int, dy: int):
        """move the images"""
        self.__dx += dx
        self.__dy += dy
        self.canvas.move(self.cell_img, dx, dy)
    
    def coord(self):
        """returns the row and column of cell"""
        return self.iy, self.ix
    
    def imcoords(self):
        """returns image coordinates"""
        return self.canvas.coords(self.cell_img)
    
    def resetmove(self):
        """to bring back the image to its original position"""
        self.canvas.move(self.cell_img, -self.__dx, -self.__dy)
        self.__dx = 0
        self.__dy = 0
