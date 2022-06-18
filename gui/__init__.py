import tkinter as tk
from tkinter import ttk
from config.const import CELLSIZE, COLOR_BORDER

from src import Brain
from gui.chessboard import ChessBoard
from config import cfg


class Game():
    
    def __init__(self):
        self.cfg: cfg = cfg()
        self.__root: tk.Tk = tk.Tk()
        self.__root.title("Chess")
        self.__root.geometry("+640+20")
        # self.self.__root.state("zoomed")

        self.display: tk.Frame = tk.Frame(
            self.__root,
            bg="#FFFFFF",
            relief=tk.SOLID,
            border=5
        )
        self.display: tk.Canvas = tk.Canvas(
            self.__root,
            bg='green',#'#7d4512',
            height=self.cfg[CELLSIZE]*8+self.cfg[COLOR_BORDER],
            width=self.cfg[CELLSIZE]*8+self.cfg[COLOR_BORDER],
            highlightthickness=0
        )
        self.display.pack()

        self.game: Brain = Brain(self.display, self.cfg)
        self.game.StartDefault()

        self.__root.bind('<Button-1>', self.game.Mouse_SLC)
        self.__root.bind('<Button-3>', self.game.Mouse_SRC)
        self.__root.bind('<B1-Motion>', self.game.MouseDrag)
        self.__root.bind('<ButtonRelease-1>', self.game.Mouse_LCR)


    def run(self):
        self.__root.mainloop()

