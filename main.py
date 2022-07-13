# -----imports-----
import tkinter as tk

from config import cfg
from src import (
    chessboard,
    ChessGrid,

)

# -----window-----
win = tk.Tk()
win.title("Chess")
win.resizable(False, False)


# -----loading-backend-----
CONFIG: cfg = cfg()


# -----interface-widgets-----
main: tk.Frame = tk.Frame(
    win,
    bg="#FFFFFF",
    relief=tk.SOLID,
    border=5
)
main.pack()

main_board = tk.Frame(main)
main_board.pack()

board: ChessBoard = ChessBoard(main_board, CONFIG)
board.canvas.pack()


# -----menu-----
menubar = tk.Menu(win)
win.config(menu=menubar)

    # def NewMenu(win, name: str):
    #     menu = tk.Menu(win.menubar, tearoff=False)
    #     menubar.add_cascade(label=name, menu=menu)
    #     return menu


# -----binding-----

win.mainloop()

