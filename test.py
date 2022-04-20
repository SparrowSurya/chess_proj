import tkinter as tk

import config as cfg
from gui.chessboard import ChessBoard
import gui.ipath as im
from src import ctxManager


root = tk.Tk()
# root.state("zoomed")

canvas = tk.Canvas(
        root,
        bg='#7d4512',
        height=cfg.SQSIZE*8+cfg.BOARD_BORDER,
        width=cfg.SQSIZE*8+cfg.BOARD_BORDER,
        highlightthickness=0
    )
canvas.pack()

board = ChessBoard(canvas)
m = ctxManager(board)

for i in range(8):
    for j in range(8):
        board.cell(i, j).newimg(tk.PhotoImage(file=im.IWQ))
        board.cell(i, j).showimg()

root.bind('<Button-1>', m.single_left_click_only)
root.bind('<Button-3>', m.single_right_click_only)

root.mainloop()

