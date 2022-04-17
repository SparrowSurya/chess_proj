import tkinter as tk

import config as cfg
from gui.chessboard import ChessBoard
from gui.pimg import *
from src import ctxManager

root = tk.Tk()
# root.state("zoomed")
root.geometry("660x660+420+10")

c = tk.Canvas(root, bg="green", height=cfg.SQSIZE*8, width=cfg.SQSIZE*8, highlightthickness=0)
c.pack(padx=10, pady=10)

z = ChessBoard(c)
m = ctxManager(z)

root.bind('<Button-1>', m.single_left_click_only)
root.bind('<Button-3>', m.single_right_click_only)

root.mainloop()