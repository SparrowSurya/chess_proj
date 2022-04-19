import tkinter as tk

import config as cfg
from gui.chessboard import ChessBoard
import gui.ipath as im
from src import ctxManager


root = tk.Tk()
# root.state("zoomed")

padd = 48
marking_font = ('times new roman', 18, 'bold')

board = tk.Canvas(root, bg='#7d4512', height=cfg.SQSIZE*8+padd, width=cfg.SQSIZE*8+padd, highlightthickness=0)
board.pack()

# horizontal marking
for i in range(8):
    x = padd//2 + (cfg.SQSIZE)*i + cfg.SQSIZE//2
    y = padd//4
    board.create_text(
        x,y, anchor=tk.CENTER, fill='white',
        text=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][i],
        font=marking_font
    )
    board.create_text(
        x, 3*y+cfg.SQSIZE*8, anchor=tk.CENTER, fill='white',
        text=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][i],
        font=marking_font
    )

# vertical marking
for i in range(8):
    x = padd//4
    y = padd//2 + (cfg.SQSIZE)*i + cfg.SQSIZE//2
    board.create_text(
        x, y, anchor=tk.CENTER, fill='white',
        text=f'{i+1}',
        font=marking_font
    )
    board.create_text(
        3*x+cfg.SQSIZE*8, y, anchor=tk.CENTER, fill='white',
        text=f'{i+1}',
        font=marking_font
    )


c = tk.Canvas(board, height=cfg.SQSIZE*8, width=cfg.SQSIZE*8, highlightthickness=0)
# c.pack(padx=10, pady=10)
c.place(x=padd//2, y=padd//2)

z = ChessBoard(c)
m = ctxManager(z)

for i in range(8):
    for j in range(8):
        z.cell(i, j).newimg(tk.PhotoImage(file=im.IWQ))
        z.cell(i, j).showimg()

root.bind('<Button-1>', m.single_left_click_only)
root.bind('<Button-3>', m.single_right_click_only)

root.mainloop()

