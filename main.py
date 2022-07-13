# -----imports-----
import tkinter as tk

from config import cfg
from src import ChessBoard, ChessGrid, Match, Image
from const import *


# -----window-----
game = tk.Tk()
game.title("Chess")
game.resizable(False, False)


# -----loading-backend-----
Config = cfg()
Grid = ChessGrid()
Img = Image()


# -----interface-widgets-----
main: tk.Frame = tk.Frame(
    game,
    bg="#FFFFFF",
    relief=tk.SOLID,
    border=5
)
main.pack()

main_board = tk.Frame(main)
main_board.pack()

chessboard: ChessBoard = ChessBoard(main_board, Config)
chessboard.canvas.pack()

match = Match(chessboard, Grid, Img)


# -----functions-----

# *mouse*
def Mouse_SLC(e: tk.Event):
    """Handles mouse single left click."""
    if match.status is not IDLE and e.widget==chessboard.board:
        match.Clicked('<SLC>', e.x, e.y)

def Mouse_LD(e: tk.Event):
    """bind event for left click drag"""
    if match.status is not IDLE and e.widget==chessboard:
        match.Clicked('<LD>', e.x, e.y)

def Mouse_LCR(e: tk.Event):
    """bind event for mouse left click release"""
    if match.status is not IDLE and e.widget==chessboard:
        match.Clicked('<LCR>', e.x, e.y)

def Mouse_SRC(e: tk.Event):
    """bind event with single right click"""
    if match.status is not IDLE and e.widget==chessboard:
        match.Clicked('<SRC>', e.x, e.y)


# -----menu-----
menubar = tk.Menu(game)
game.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=False)
options_menu = tk.Menu(menubar, tearoff=False)

menubar.add_cascade(label='File', menu=file_menu)
menubar.add_cascade(label='Options', menu=options_menu)

file_menu.add_command(label='New')
file_menu.add_command(label='Open')
file_menu.add_separator()
file_menu.add_command(label='Save')
file_menu.add_separator()
file_menu.add_command(label='Settings')
file_menu.add_separator()
file_menu.add_command(label='Exit', command=game.quit)

options_menu.add_command(label='Play', command=lambda: match.Start(DEFAULT_GRID))



# -----binding-----
game.bind("<Button-1>", Mouse_SLC)


game.mainloop()
