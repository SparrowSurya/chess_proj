import tkinter as tk
import config as cfg
from config.const import NULL

class Cell:
    def __init__(self, canvas: tk.Canvas, row: int, column: int, fill: str, image=""):
        self.canvas: tk.Canvas = canvas
        self.ix: int = column
        self.iy: int = row
        self.pid: str = NULL
        self.selected: bool = False

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
            width=2,
        )

        self.cell_img = self.canvas.create_image(
            (2*self.ix +1)*cfg.SQSIZE //2,
            (2*self.iy +1)*cfg.SQSIZE //2,
            anchor=tk.CENTER,
            state=tk.NORMAL,
            image=self.img
        )
    
    def select(self, fill_color: str):
        self.canvas.itemconfig(self.cell_col, fill=fill_color)
        self.selected = True
    
    def deselect(self):
        self.canvas.itemconfig(self.cell_col, fill=self.fill)
        self.selected = False
    
    def activecol(self):
        return self.canvas.itemcget(self.cell_col, 'fill')
    
    def newimg(self, image, pid):
        self.img = image
        self.pid = pid
        self.canvas.itemconfig(self.cell_img, image=self.img)
        self.canvas.tag_raise(self.cell_img)
    
    def showimg(self):
        self.canvas.itemconfig(self.cell_img, state=tk.NORMAL)
        self.canvas.tag_raise(self.cell_img)
    
    def hideimg(self):
        self.canvas.itemconfig(self.cell_img, state=tk.HIDDEN)
    
    def clearimg(self):
        self.canvas.itemconfig(self.cell_img, image="")
        self.img = ""
        self.pid = NULL
    
    def move(self, dx: int, dy: int):
        self.__dx += dx
        self.__dy += dy
        self.canvas.move(self.cell_img, self.__dx, self.__dy)
    
    def resetmove(self):
        self.canvas.move(self.cell_img, -self.__dx, -self.__dy)
        self.__dx = 0
        self.__dy = 0
