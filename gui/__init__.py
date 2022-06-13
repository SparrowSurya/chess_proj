import tkinter as tk
from tkinter import ttk

from src import Brain
from gui.chessboard import ChessBoard
import config as cfg


class Game():
    
    def __init__(self):
        self.__root: tk.Tk = tk.Tk()
        self.__root.title("Chess")
        self.__root.geometry("+640+20")
        # self.self.__root.state("zoomed")

        self.viewport: tk.Canvas = tk.Canvas(
            self.__root,
            bg='#7d4512',
            height=cfg.SQSIZE*8+cfg.BOARD_BORDER,
            width=cfg.SQSIZE*8+cfg.BOARD_BORDER,
            highlightthickness=0
        )
        self.viewport.pack()

        self.board: ChessBoard = ChessBoard(self.viewport)
        self.game: Brain = Brain(self.board)
        self.game.StartDefault()

        self.__root.bind('<Button-1>', self.game.Mouse_SLC)
        self.__root.bind('<Button-3>', self.game.Mouse_SRC)
        self.__root.bind('<B1-Motion>', self.game.MouseDrag)
        self.__root.bind('<ButtonRelease-1>', self.game.Mouse_LCR)


    def run(self):
        self.__root.mainloop()

    def config(self, key: str, value: str, **kwargs):
        """method to configure the game with proper gui change and attribute update"""
        pass