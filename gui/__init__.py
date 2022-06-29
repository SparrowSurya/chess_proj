import tkinter as tk
from config.const import BORDER_WIDTH, CELLSIZE

from gui.chessboard import ChessBoard
from config import cfg


class GUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Chess")
        self.resizable(False, False)

        self.cfg: cfg = cfg()

        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # basic container
        self._main: tk.Frame = tk.Frame(
            self,
            bg="#FFFFFF",
            relief=tk.SOLID,
            border=5
        )
        self._main.pack()

        # chessboard lies in this widget
        self._main_board = tk.Frame(
            self._main,
            bg='orange',#'#7d4512',
        )
        self._main_board.pack()

        self.chessboard: ChessBoard = ChessBoard(self._main_board, self.cfg)
        self.chessboard.canvas.pack()


    def NewMenu(self, name: str):
        menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label=name, menu=menu)
        return menu