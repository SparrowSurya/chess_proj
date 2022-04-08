import tkinter as tk
from configs.gui import *

class Cell:
    def __init__(self, canvas: tk.Canvas, row: int, column: int, size: int, fill: str, edge: str):
        self.canvas: tk.Canvas = canvas
        self.ix: int = column
        self.iy: int = row
        self.size: int = size
        self.fill: str = fill
        self.edge: str = edge

        self.__dx: int = 0
        self.__dy: int = 0
        
        self.__img = None
        self.cell_bg = self.canvas.create_rectangle(
            self.ix*self.size,
            self.iy*self.size,
            (self.ix+1)*self.size,
            (self.iy+1)*self.size,
            fill=self.fill,
            width=0,
        )

        self.cell_fg = self.canvas.create_rectangle(
            self.ix*self.size +2,
            self.iy*self.size +2,
            (self.ix+1)*self.size -2,
            (self.iy+1)*self.size -2,
            fill=self.fill,
            width=0,
        )
        
        self.cell_im = self.canvas.create_image(
            (2*self.ix +1)*self.size //2,
            (2*self.iy +1)*self.size //2,
            anchor=tk.CENTER,
            state=tk.NORMAL,
        )
    
    def select(self, color: str):
        self.canvas.itemconfig(self.cell_fg, fill=color)
        self.canvas.itemconfig(self.cell_bg, fill="black")
    
    def deselect(self):
        self.canvas.itemconfig(self.cell_fg, fill=self.fill)
        self.canvas.itemconfig(self.cell_bg, fill=self.fill)
    
    def newimg(self, image):
        self.__img = image
        self.canvas.itemconfig(self.cell_im, image=self.__img)
    
    def showimg(self):
        self.canvas.itemconfig(self.cell_im, state=tk.NORMAL)
    
    def hideimg(self):
        self.canvas.itemconfig(self.cell_im, state=tk.HIDDEN)

    def move(self, dx, dy):
        self.__dx += dx
        self.__dy += dy
        self.canvas.move(self.cell_im, self.__dx, self.__dy)
    
    def resetmove(self):
        self.canvas.move(self.cell_im, -self.__dx, -self.__dy)
        self.__dx = 0
        self.__dy = 0
