import tkinter as tk
from gui.chessboard import ChessBoard
from src import ctxManager


root = tk.Tk()
root.state("zoomed")

c = tk.Canvas(root, bg="green")
c.pack(fill=tk.BOTH, expand=1)

z = ChessBoard(c)

m = ctxManager(z)

root.bind('<Button-1>', m.single_left_click_only)
root.bind('<Button-3>', m.single_right_click_only)

root.mainloop()