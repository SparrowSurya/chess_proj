import tkinter as tk

import config as cfg
from gui.chessboard import ChessBoard
import gui.ipath as im
from src import ctxManager


root = tk.Tk()
# root.state("zoomed")
root.geometry("660x660+420+10")
root.config(bg='green')

c = tk.Canvas(root, height=cfg.SQSIZE*8, width=cfg.SQSIZE*8, highlightthickness=0)
c.pack(padx=10, pady=10)

z = ChessBoard(c)
m = ctxManager(z)

# for i in range(8):
#     for j in range(8):
#         z.cell(i, j).newimg(tk.PhotoImage(im.IWP))
#         z.cell(i, j).showimg()

root.bind('<Button-1>', m.single_left_click_only)
root.bind('<Button-3>', m.single_right_click_only)

root.mainloop()