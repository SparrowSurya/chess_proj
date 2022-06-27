import tkinter as tk
from config.const import BORDER_WIDTH, CELLSIZE

from gui.chessboard import ChessBoard
from config import cfg


class GUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Chess")

        self.cfg: cfg = cfg()

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
            height=CELLSIZE*8+BORDER_WIDTH,
            width=CELLSIZE*8+BORDER_WIDTH,
            highlightthickness=0
        )
        self._main_board.pack()

        self.chessboard: ChessBoard = ChessBoard(self._main_board, self.cfg)
        self.chessboard.canvas.pack()

    