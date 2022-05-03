import tkinter as tk

import config as cfg
from gui.chessboard import ChessBoard
from src import Brain


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
b = Brain(board)

root.bind('<Button-1>', b.Mouse_SLC)
root.bind('<Button-3>', b.Mouse_SRC)
root.bind('<Escape>', b.StartDefault)

root.mainloop()
